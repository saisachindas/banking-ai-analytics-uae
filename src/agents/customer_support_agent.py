"""
Agentic AI - Customer Support Agent

Intelligent agent for handling customer support requests using LangChain,
with tools for account lookup, transaction history, and complaint management.
"""

import logging
from typing import Any, Dict
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


class CustomerSupportAgent:
    """
    Autonomous agent for customer support using LangChain.
    """
    
    def __init__(self):
        """
        Initialize the customer support agent with tools.
        """
        self.agent = None
        self.tools = self._create_tools()
        self._initialize_agent()
    
    def _create_tools(self) -> list:
        """
        Create tools for the agent.
        
        Returns:
            list: List of Tool objects
        """
        tools = [
            Tool(
                name="get_account_balance",
                func=self._get_account_balance,
                description="Get current account balance for a customer. Input: customer_id"
            ),
            Tool(
                name="get_recent_transactions",
                func=self._get_recent_transactions,
                description="Get last 5 transactions for a customer. Input: customer_id"
            ),
            Tool(
                name="raise_complaint",
                func=self._raise_complaint,
                description="Raise a new complaint. Input: customer_id|category|description"
            ),
            Tool(
                name="check_card_status",
                func=self._check_card_status,
                description="Check credit card status. Input: customer_id"
            )
        ]
        return tools
    
    def _get_account_balance(self, customer_id: str) -> str:
        """
        Get account balance for a customer.
        
        Args:
            customer_id: Customer ID
        
        Returns:
            str: Account balance information
        """
        try:
            customer_id = int(customer_id)
            db = SessionLocal()
            
            query = text(f"""
                SELECT 
                    c.customer_name,
                    a.account_number,
                    a.current_balance_aed,
                    a.available_balance_aed,
                    p.product_name
                FROM ACCOUNTS a
                JOIN CUSTOMERS c ON a.customer_id = c.customer_id
                JOIN PRODUCTS p ON a.product_id = p.product_id
                WHERE c.customer_id = {customer_id}
                LIMIT 1
            """)
            
            result = db.execute(query).fetchone()
            db.close()
            
            if result:
                data = dict(result._mapping)
                return f"Account {data['account_number']}: Balance AED {data['current_balance_aed']:,.2f}, Available: AED {data['available_balance_aed']:,.2f}"
            return f"No account found for customer {customer_id}"
        
        except Exception as e:
            logger.error(f"Error getting account balance: {e}")
            return f"Error retrieving balance: {str(e)}"
    
    def _get_recent_transactions(self, customer_id: str) -> str:
        """
        Get recent transactions for a customer.
        
        Args:
            customer_id: Customer ID
        
        Returns:
            str: Recent transaction details
        """
        try:
            customer_id = int(customer_id)
            db = SessionLocal()
            
            query = text(f"""
                SELECT 
                    transaction_date,
                    transaction_type,
                    transaction_amount_aed,
                    merchant_name,
                    channel
                FROM TRANSACTIONS
                WHERE customer_id = {customer_id}
                ORDER BY transaction_date DESC
                LIMIT 5
            """)
            
            results = db.execute(query).fetchall()
            db.close()
            
            if not results:
                return f"No transactions found for customer {customer_id}"
            
            txn_summary = "Recent transactions:\n"
            for row in results:
                data = dict(row._mapping)
                txn_summary += f"- {data['transaction_date']}: {data['transaction_type']} AED {data['transaction_amount_aed']:,.2f} at {data['merchant_name']} via {data['channel']}\n"
            
            return txn_summary
        
        except Exception as e:
            logger.error(f"Error getting transactions: {e}")
            return f"Error retrieving transactions: {str(e)}"
    
    def _raise_complaint(self, input_str: str) -> str:
        """
        Raise a new complaint.
        
        Args:
            input_str: Format: customer_id|category|description
        
        Returns:
            str: Complaint confirmation
        """
        try:
            parts = input_str.split("|")
            if len(parts) < 3:
                return "Invalid input. Format: customer_id|category|description"
            
            customer_id = int(parts[0])
            category = parts[1]
            description = parts[2]
            
            db = SessionLocal()
            
            # Get branch_id for the customer
            branch_query = text(f"SELECT branch_id FROM ACCOUNTS WHERE customer_id = {customer_id} LIMIT 1")
            branch_result = db.execute(branch_query).fetchone()
            branch_id = branch_result[0] if branch_result else 1
            
            # Insert complaint
            insert_query = text(f"""
                INSERT INTO COMPLAINTS 
                (customer_id, branch_id, complaint_date, complaint_time, complaint_category, complaint_description, severity, status)
                VALUES ({customer_id}, {branch_id}, CURRENT_DATE, CURRENT_TIME, '{category}', '{description}', 'Medium', 'Open')
            """)
            
            db.execute(insert_query)
            db.commit()
            db.close()
            
            return f"Complaint raised successfully for customer {customer_id}. Category: {category}"
        
        except Exception as e:
            logger.error(f"Error raising complaint: {e}")
            return f"Error raising complaint: {str(e)}"
    
    def _check_card_status(self, customer_id: str) -> str:
        """
        Check card status for a customer.
        
        Args:
            customer_id: Customer ID
        
        Returns:
            str: Card status information
        """
        try:
            customer_id = int(customer_id)
            db = SessionLocal()
            
            query = text(f"""
                SELECT 
                    card_brand,
                    card_type,
                    card_status,
                    credit_limit_aed,
                    current_balance_aed,
                    expiry_date
                FROM CARDS
                WHERE customer_id = {customer_id}
                LIMIT 1
            """)
            
            result = db.execute(query).fetchone()
            db.close()
            
            if result:
                data = dict(result._mapping)
                return f"Card: {data['card_brand']} {data['card_type']}, Status: {data['card_status']}, Limit: AED {data['credit_limit_aed']:,.2f}, Balance: AED {data['current_balance_aed']:,.2f}"
            
            return f"No card found for customer {customer_id}"
        
        except Exception as e:
            logger.error(f"Error checking card status: {e}")
            return f"Error checking card: {str(e)}"
    
    def _initialize_agent(self):
        """
        Initialize the LangChain agent.
        """
        if not LANGCHAIN_AVAILABLE:
            logger.warning("LangChain not available. Agent will use mock responses.")
            return
        
        try:
            logger.info("Initializing customer support agent...")
            
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
            
            logger.info("Customer support agent initialized successfully")
        
        except Exception as e:
            logger.error(f"Error initializing agent: {e}")
    
    def handle_request(self, customer_id: int, request: str) -> str:
        """
        Handle a customer support request.
        
        Args:
            customer_id: Customer ID
            request: Customer's request
        
        Returns:
            str: Agent's response
        
        Examples:
            agent = CustomerSupportAgent()
            response = agent.handle_request(1, "What is my account balance?")
        """
        if not self.agent:
            # Fallback to mock response
            return self._mock_response(customer_id, request)
        
        try:
            logger.info(f"Handling request for customer {customer_id}: {request}")
            prompt = f"Customer {customer_id} asks: {request}"
            response = self.agent.run(prompt)
            return response
        
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return self._mock_response(customer_id, request)
    
    def _mock_response(self, customer_id: int, request: str) -> str:
        """
        Provide mock response when agent is not available.
        
        Args:
            customer_id: Customer ID
            request: Customer request
        
        Returns:
            str: Mock response
        """
        if "balance" in request.lower():
            return f"Your current account balance is AED 150,000 with AED 150,000 available. (Mock response)"
        elif "transaction" in request.lower():
            return f"Your last 5 transactions include purchases at Carrefour, DEWA payment, and a salary deposit. (Mock response)"
        elif "complaint" in request.lower():
            return f"Your complaint has been registered with our support team. We will follow up within 24 hours. (Mock response)"
        else:
            return f"Thank you for contacting us. How can we assist you further? (Mock response)"


if __name__ == "__main__":
    # Initialize and test the agent
    agent = CustomerSupportAgent()
    
    print("\n=== Customer Support Agent ===")
    
    # Example requests
    requests = [
        (1, "What is my account balance?"),
        (1, "Show me my recent transactions"),
        (2, "I want to raise a complaint about delayed transfer")
    ]
    
    for customer_id, request in requests:
        print(f"\nCustomer {customer_id}: {request}")
        response = agent.handle_request(customer_id, request)
        print(f"Agent: {response}")
