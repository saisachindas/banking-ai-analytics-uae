"""
Agentic AI - Fraud Investigation Agent

Intelligent agent for investigating suspicious transactions and generating
fraud investigation reports.
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


class FraudInvestigationAgent:
    """
    Autonomous agent for fraud investigation using LangChain.
    """
    
    def __init__(self):
        """
        Initialize the fraud investigation agent with tools.
        """
        self.agent = None
        self.tools = self._create_tools()
        self._initialize_agent()
    
    def _create_tools(self) -> list:
        """
        Create tools for fraud investigation.
        
        Returns:
            list: List of Tool objects
        """
        tools = [
            Tool(
                name="get_flagged_transactions",
                func=self._get_flagged_transactions,
                description="Get flagged suspicious transactions above a minimum amount. Input: min_amount_aed"
            ),
            Tool(
                name="get_customer_risk_profile",
                func=self._get_customer_risk_profile,
                description="Get customer risk profile and assessment. Input: customer_id"
            ),
            Tool(
                name="get_transaction_pattern",
                func=self._get_transaction_pattern,
                description="Analyze transaction patterns for a customer. Input: customer_id"
            ),
            Tool(
                name="flag_account_for_review",
                func=self._flag_account_for_review,
                description="Flag an account for manual review. Input: customer_id|reason"
            )
        ]
        return tools
    
    def _get_flagged_transactions(self, min_amount: str) -> str:
        """
        Get flagged transactions above a minimum amount.
        
        Args:
            min_amount: Minimum transaction amount in AED
        
        Returns:
            str: Flagged transactions summary
        """
        try:
            min_amount = float(min_amount)
            db = SessionLocal()
            
            query = text(f"""
                SELECT 
                    t.transaction_id,
                    t.customer_id,
                    c.customer_name,
                    t.transaction_date,
                    t.transaction_amount_aed,
                    t.channel,
                    t.merchant_name,
                    t.fraud_flag,
                    t.fraud_score
                FROM TRANSACTIONS t
                JOIN CUSTOMERS c ON t.customer_id = c.customer_id
                WHERE t.transaction_amount_aed >= {min_amount}
                AND (t.fraud_flag = TRUE OR t.fraud_score > 50)
                ORDER BY t.fraud_score DESC
                LIMIT 10
            """)
            
            results = db.execute(query).fetchall()
            db.close()
            
            if not results:
                return f"No flagged transactions found above AED {min_amount}"
            
            summary = f"Found {len(results)} suspicious transactions above AED {min_amount}:\n"
            for row in results:
                data = dict(row._mapping)
                summary += f"- ID {data['transaction_id']}: {data['customer_name']} - AED {data['transaction_amount_aed']:,.2f} at {data['merchant_name']} (Score: {data['fraud_score']}%)\n"
            
            return summary
        
        except Exception as e:
            logger.error(f"Error getting flagged transactions: {e}")
            return f"Error retrieving flagged transactions: {str(e)}"
    
    def _get_customer_risk_profile(self, customer_id: str) -> str:
        """
        Get customer risk profile.
        
        Args:
            customer_id: Customer ID
        
        Returns:
            str: Risk profile information
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
                    COUNT(DISTINCT l.loan_id) as loan_count,
                    COUNT(DISTINCT CASE WHEN l.npl_flag = TRUE THEN l.loan_id END) as npl_count
                FROM CUSTOMERS c
                LEFT JOIN RISK_FACTORS rf ON c.customer_id = rf.customer_id
                LEFT JOIN LOANS l ON c.customer_id = l.customer_id
                WHERE c.customer_id = {customer_id}
                GROUP BY c.customer_id, c.customer_name, c.aml_risk_score, c.pep_flag, c.sanctions_flag,
                         rf.risk_level, rf.risk_score, rf.risk_type
            """)
            
            result = db.execute(query).fetchone()
            db.close()
            
            if not result:
                return f"No customer found with ID {customer_id}"
            
            data = dict(result._mapping)
            profile = f"Customer: {data['customer_name']}\n"
            profile += f"AML Risk Score: {data['aml_risk_score']}/100\n"
            profile += f"PEP Flag: {data['pep_flag']}\n"
            profile += f"Sanctions Flag: {data['sanctions_flag']}\n"
            profile += f"Risk Level: {data['risk_level']}\n"
            profile += f"Loans: {data['loan_count']} (NPL: {data['npl_count']})\n"
            
            return profile
        
        except Exception as e:
            logger.error(f"Error getting risk profile: {e}")
            return f"Error retrieving risk profile: {str(e)}"
    
    def _get_transaction_pattern(self, customer_id: str) -> str:
        """
        Analyze transaction patterns.
        
        Args:
            customer_id: Customer ID
        
        Returns:
            str: Transaction pattern analysis
        """
        try:
            customer_id = int(customer_id)
            db = SessionLocal()
            
            query = text(f"""
                SELECT 
                    COUNT(*) as total_txns,
                    SUM(transaction_amount_aed) as total_value,
                    AVG(transaction_amount_aed) as avg_value,
                    MAX(transaction_amount_aed) as max_value,
                    COUNT(DISTINCT channel) as unique_channels,
                    COUNT(DISTINCT merchant_name) as unique_merchants,
                    SUM(CASE WHEN fraud_flag = TRUE THEN 1 ELSE 0 END) as flagged_count
                FROM TRANSACTIONS
                WHERE customer_id = {customer_id}
                AND transaction_date >= CURRENT_DATE - INTERVAL '90 days'
            """)
            
            result = db.execute(query).fetchone()
            db.close()
            
            if not result:
                return f"No transaction history for customer {customer_id}"
            
            data = dict(result._mapping)
            pattern = f"Transaction Pattern (Last 90 days):\n"
            pattern += f"- Total transactions: {data['total_txns']}\n"
            pattern += f"- Total value: AED {data['total_value']:,.2f}\n"
            pattern += f"- Average value: AED {data['avg_value']:,.2f}\n"
            pattern += f"- Max value: AED {data['max_value']:,.2f}\n"
            pattern += f"- Flagged transactions: {data['flagged_count']}\n"
            
            return pattern
        
        except Exception as e:
            logger.error(f"Error analyzing transaction pattern: {e}")
            return f"Error analyzing pattern: {str(e)}"
    
    def _flag_account_for_review(self, input_str: str) -> str:
        """
        Flag an account for manual review.
        
        Args:
            input_str: Format: customer_id|reason
        
        Returns:
            str: Confirmation message
        """
        try:
            parts = input_str.split("|")
            if len(parts) < 2:
                return "Invalid input. Format: customer_id|reason"
            
            customer_id = int(parts[0])
            reason = parts[1]
            
            logger.warning(f"Account {customer_id} flagged for review. Reason: {reason}")
            
            return f"Account {customer_id} has been flagged for manual review. Reason: {reason}"
        
        except Exception as e:
            logger.error(f"Error flagging account: {e}")
            return f"Error flagging account: {str(e)}"
    
    def _initialize_agent(self):
        """
        Initialize the LangChain agent.
        """
        if not LANGCHAIN_AVAILABLE:
            logger.warning("LangChain not available. Agent will use mock responses.")
            return
        
        try:
            logger.info("Initializing fraud investigation agent...")
            
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
            
            logger.info("Fraud investigation agent initialized successfully")
        
        except Exception as e:
            logger.error(f"Error initializing agent: {e}")
    
    def investigate(self, min_amount: float = 10000) -> str:
        """
        Investigate fraud for transactions above a threshold.
        
        Args:
            min_amount: Minimum transaction amount to investigate
        
        Returns:
            str: Investigation report
        
        Examples:
            agent = FraudInvestigationAgent()
            report = agent.investigate(min_amount=10000)
        """
        if not self.agent:
            return self._mock_investigation_report(min_amount)
        
        try:
            logger.info(f"Starting fraud investigation for amounts >= AED {min_amount}")
            prompt = f"Generate a fraud investigation report for all suspicious transactions above AED {min_amount}"
            report = self.agent.run(prompt)
            return report
        
        except Exception as e:
            logger.error(f"Error during investigation: {e}")
            return self._mock_investigation_report(min_amount)
    
    def _mock_investigation_report(self, min_amount: float) -> str:
        """
        Provide mock investigation report.
        
        Args:
            min_amount: Minimum amount
        
        Returns:
            str: Mock report
        """
        return f"""
        === FRAUD INVESTIGATION REPORT ===
        Investigation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Threshold: AED {min_amount:,.2f}
        
        FINDINGS:
        - 3 high-risk transactions identified
        - 2 accounts flagged for review
        - 1 customer requires enhanced monitoring
        
        RECOMMENDATIONS:
        1. Contact customers for verification
        2. Review transaction patterns
        3. Monitor future activity
        
        (Mock Report)
        """


if __name__ == "__main__":
    # Initialize and test the agent
    agent = FraudInvestigationAgent()
    
    print("\n=== Fraud Investigation Agent ===")
    report = agent.investigate(min_amount=5000)
    print(report)
