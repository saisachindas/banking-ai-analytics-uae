"""
Agentic AI - Compliance Agent

Intelligent agent for monitoring compliance, KYC status, AML risk,
and document expiration across the customer portfolio.
"""

import logging
from typing import List, Dict
from sqlalchemy import text
from datetime import datetime, timedelta

try:
    from langchain.agents import initialize_agent, Tool, AgentType
    from langchain.llms.huggingface_pipeline import HuggingFacePipeline
    from transformers import pipeline as hf_pipeline
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    logging.warning("LangChain not fully installed. Agent features limited.")

from src.db.connection import SessionLocal

logger = logging.getLogger(__name__)


class ComplianceAgent:
    """
    Autonomous agent for compliance monitoring using LangChain.
    """
    
    def __init__(self):
        """
        Initialize the compliance agent with tools.
        """
        self.agent = None
        self.tools = self._create_tools()
        self._initialize_agent()
    
    def _create_tools(self) -> list:
        """
        Create tools for compliance monitoring.
        
        Returns:
            list: List of Tool objects
        """
        tools = [
            Tool(
                name="get_kyc_status",
                func=self._get_kyc_status,
                description="Get KYC status for a customer. Input: customer_id"
            ),
            Tool(
                name="get_aml_risk",
                func=self._get_aml_risk,
                description="Get AML risk assessment. Input: customer_id"
            ),
            Tool(
                name="list_expiring_documents",
                func=self._list_expiring_documents,
                description="List documents expiring within N days. Input: days"
            ),
            Tool(
                name="get_compliance_dashboard",
                func=self._get_compliance_dashboard,
                description="Get overall compliance dashboard metrics. Input: empty"
            )
        ]
        return tools
    
    def _get_kyc_status(self, customer_id: str) -> str:
        """
        Get KYC status for a customer.
        
        Args:
            customer_id: Customer ID
        
        Returns:
            str: KYC status information
        """
        try:
            customer_id = int(customer_id)
            db = SessionLocal()
            
            query = text(f"""
                SELECT 
                    c.customer_name,
                    c.kyc_status,
                    c.kyc_completion_date,
                    COUNT(DISTINCT CASE WHEN kd.verification_status = 'Verified' THEN kd.document_id END) as verified_docs,
                    COUNT(DISTINCT CASE WHEN kd.verification_status = 'Pending' THEN kd.document_id END) as pending_docs,
                    COUNT(DISTINCT CASE WHEN kd.verification_status = 'Expired' THEN kd.document_id END) as expired_docs
                FROM CUSTOMERS c
                LEFT JOIN KYC_DOCUMENTS kd ON c.customer_id = kd.customer_id
                WHERE c.customer_id = {customer_id}
                GROUP BY c.customer_id, c.customer_name, c.kyc_status, c.kyc_completion_date
            """)
            
            result = db.execute(query).fetchone()
            db.close()
            
            if not result:
                return f"No customer found with ID {customer_id}"
            
            data = dict(result._mapping)
            status = f"KYC Status - {data['customer_name']}:\n"
            status += f"Status: {data['kyc_status']}\n"
            status += f"Completion Date: {data['kyc_completion_date']}\n"
            status += f"Documents - Verified: {data['verified_docs']}, Pending: {data['pending_docs']}, Expired: {data['expired_docs']}\n"
            
            return status
        
        except Exception as e:
            logger.error(f"Error getting KYC status: {e}")
            return f"Error retrieving KYC status: {str(e)}"
    
    def _get_aml_risk(self, customer_id: str) -> str:
        """
        Get AML risk assessment for a customer.
        
        Args:
            customer_id: Customer ID
        
        Returns:
            str: AML risk information
        """
        try:
            customer_id = int(customer_id)
            db = SessionLocal()
            
            query = text(f"""
                SELECT 
                    c.customer_name,
                    c.aml_risk_score,
                    c.pep_flag,
                    c.sanctions_flag,
                    rf.risk_level,
                    rf.risk_score,
                    rf.risk_type,
                    rf.last_review_date,
                    rf.next_review_date,
                    rf.monitoring_frequency
                FROM CUSTOMERS c
                LEFT JOIN RISK_FACTORS rf ON c.customer_id = rf.customer_id AND rf.risk_type = 'Compliance Risk'
                WHERE c.customer_id = {customer_id}
            """)
            
            result = db.execute(query).fetchone()
            db.close()
            
            if not result:
                return f"No customer found with ID {customer_id}"
            
            data = dict(result._mapping)
            
            aml = f"AML Risk Assessment - {data['customer_name']}:\n"
            aml += f"Risk Score: {data['aml_risk_score']}/100\n"
            aml += f"Risk Level: {data['risk_level']}\n"
            aml += f"PEP Flag: {'YES' if data['pep_flag'] else 'NO'}\n"
            aml += f"Sanctions Flag: {'YES' if data['sanctions_flag'] else 'NO'}\n"
            aml += f"Monitoring Frequency: {data['monitoring_frequency']}\n"
            aml += f"Last Review: {data['last_review_date']}\n"
            
            return aml
        
        except Exception as e:
            logger.error(f"Error getting AML risk: {e}")
            return f"Error retrieving AML risk: {str(e)}"
    
    def _list_expiring_documents(self, days: str) -> str:
        """
        List documents expiring within N days.
        
        Args:
            days: Number of days
        
        Returns:
            str: List of expiring documents
        """
        try:
            days = int(days)
            db = SessionLocal()
            
            cutoff_date = (datetime.now() + timedelta(days=days)).date()
            
            query = text(f"""
                SELECT 
                    kd.document_id,
                    c.customer_name,
                    kd.document_type,
                    kd.expiry_date,
                    (kd.expiry_date - CURRENT_DATE) as days_until_expiry
                FROM KYC_DOCUMENTS kd
                JOIN CUSTOMERS c ON kd.customer_id = c.customer_id
                WHERE kd.expiry_date <= '{cutoff_date}'
                AND kd.expiry_date > CURRENT_DATE
                AND kd.verification_status = 'Verified'
                ORDER BY kd.expiry_date ASC
            """)
            
            results = db.execute(query).fetchall()
            db.close()
            
            if not results:
                return f"No documents expiring within {days} days"
            
            expiring = f"Documents expiring within {days} days:\n"
            for row in results:
                data = dict(row._mapping)
                expiring += f"- {data['customer_name']}: {data['document_type']} expires in {data['days_until_expiry']} days ({data['expiry_date']})\n"
            
            return expiring
        
        except Exception as e:
            logger.error(f"Error listing expiring documents: {e}")
            return f"Error retrieving expiring documents: {str(e)}"
    
    def _get_compliance_dashboard(self, _: str = "") -> str:
        """
        Get overall compliance dashboard metrics.
        
        Args:
            _: Unused parameter
        
        Returns:
            str: Dashboard metrics
        """
        try:
            db = SessionLocal()
            
            query = text("""
                SELECT 
                    COUNT(DISTINCT customer_id) as total_customers,
                    SUM(CASE WHEN kyc_status = 'Verified' THEN 1 ELSE 0 END) as kyc_verified,
                    SUM(CASE WHEN kyc_status = 'Pending' THEN 1 ELSE 0 END) as kyc_pending,
                    SUM(CASE WHEN aml_risk_score > 75 THEN 1 ELSE 0 END) as high_risk_aml,
                    SUM(CASE WHEN pep_flag = TRUE THEN 1 ELSE 0 END) as pep_count,
                    SUM(CASE WHEN sanctions_flag = TRUE THEN 1 ELSE 0 END) as sanctions_count
                FROM CUSTOMERS
            """)
            
            result = db.execute(query).fetchone()
            db.close()
            
            if not result:
                return "No customer data available"
            
            data = dict(result._mapping)
            
            dashboard = f"\n=== COMPLIANCE DASHBOARD ==="
            dashboard += f"\nTotal Customers: {data['total_customers']}\n"
            dashboard += f"KYC Status:\n"
            dashboard += f"  - Verified: {data['kyc_verified']}\n"
            dashboard += f"  - Pending: {data['kyc_pending']}\n"
            dashboard += f"High Risk (AML Score > 75): {data['high_risk_aml']}\n"
            dashboard += f"PEP Count: {data['pep_count']}\n"
            dashboard += f"Sanctions Flag: {data['sanctions_count']}\n"
            
            return dashboard
        
        except Exception as e:
            logger.error(f"Error getting compliance dashboard: {e}")
            return f"Error retrieving dashboard: {str(e)}"
    
    def _initialize_agent(self):
        """
        Initialize the LangChain agent.
        """
        if not LANGCHAIN_AVAILABLE:
            logger.warning("LangChain not available. Agent will use mock responses.")
            return
        
        try:
            logger.info("Initializing compliance agent...")
            
            # Create LLM
            llm_pipeline = hf_pipeline(
                "text2text-generation",
                model="google/flan-t5-base",
                device=-1
            )
            
            llm = HuggingFacePipeline(
                model_kwargs={"temperature": 0.1},
                pipeline=llm_pipeline
            )
            
            # Initialize agent
            self.agent = initialize_agent(
                self.tools,
                llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                max_iterations=5
            )
            
            logger.info("Compliance agent initialized successfully")
        
        except Exception as e:
            logger.error(f"Error initializing agent: {e}")
    
    def generate_report(self, scope: str = "portfolio") -> str:
        """
        Generate a compliance report.
        
        Args:
            scope: Report scope (portfolio, high-risk, etc.)
        
        Returns:
            str: Compliance report
        
        Examples:
            agent = ComplianceAgent()
            report = agent.generate_report(scope="portfolio")
        """
        if not self.agent:
            return self._mock_compliance_report(scope)
        
        try:
            logger.info(f"Generating compliance report for {scope}")
            prompt = f"Generate a comprehensive compliance report for the {scope}. Include KYC status, AML risks, and document expiry."
            report = self.agent.run(prompt)
            return report
        
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return self._mock_compliance_report(scope)
    
    def _mock_compliance_report(self, scope: str) -> str:
        """
        Provide mock compliance report.
        
        Args:
            scope: Report scope
        
        Returns:
            str: Mock report
        """
        return f"""
        === COMPLIANCE REPORT ({scope.upper()}) ===
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        EXECUTIVE SUMMARY:
        - Total Customers: 8
        - KYC Verified: 8 (100%)
        - High Risk (AML): 2
        - PEP Count: 1
        - Sanctions Flags: 0
        
        KEY FINDINGS:
        1. All customers have completed KYC
        2. 2 customers require enhanced monitoring
        3. No critical compliance issues
        4. 5 documents expiring within 90 days
        
        RECOMMENDATIONS:
        1. Review KYC for PEP customer monthly
        2. Update expiring documents
        3. Continue standard monitoring for low-risk customers
        
        (Mock Report)
        """


if __name__ == "__main__":
    # Initialize and test the agent
    agent = ComplianceAgent()
    
    print("\n=== Compliance Agent ===")
    report = agent.generate_report(scope="portfolio")
    print(report)
