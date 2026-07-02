#!/usr/bin/env python
"""
Run Compliance Agent
"""

import sys
import logging
from src.agents.compliance_agent import ComplianceAgent

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
)

if __name__ == "__main__":
    try:
        print("\n" + "="*60)
        print("COMPLIANCE AGENT")
        print("="*60)
        
        agent = ComplianceAgent()
        report = agent.generate_report(scope="portfolio")
        print(report)
        
        print("\n✓ Compliance agent test completed!")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
