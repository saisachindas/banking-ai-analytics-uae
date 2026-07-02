#!/usr/bin/env python
"""
Run Fraud Investigation Agent
"""

import sys
import logging
from src.agents.fraud_investigation_agent import FraudInvestigationAgent

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
)

if __name__ == "__main__":
    try:
        print("\n" + "="*60)
        print("FRAUD INVESTIGATION AGENT")
        print("="*60)
        
        agent = FraudInvestigationAgent()
        report = agent.investigate(min_amount=5000)
        print(report)
        
        print("\n✓ Fraud investigation agent test completed!")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
