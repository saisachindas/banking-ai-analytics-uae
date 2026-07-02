#!/usr/bin/env python
"""
Run Customer Support Agent
"""

import sys
import logging
from src.agents.customer_support_agent import CustomerSupportAgent

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
)

if __name__ == "__main__":
    try:
        print("\n" + "="*60)
        print("CUSTOMER SUPPORT AGENT")
        print("="*60)
        
        agent = CustomerSupportAgent()
        
        # Example support requests
        test_requests = [
            (1, "What is my account balance?"),
            (1, "Show me my recent transactions"),
            (2, "I want to raise a complaint")
        ]
        
        for customer_id, request in test_requests:
            print(f"\nCustomer {customer_id}: {request}")
            response = agent.handle_request(customer_id, request)
            print(f"Agent: {response}")
        
        print("\n✓ Customer support agent test completed!")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
