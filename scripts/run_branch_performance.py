#!/usr/bin/env python
"""
Run Branch Performance Analysis
"""

import sys
import logging
from src.analytics.branch_performance import analyze_branch_performance, print_branch_performance_summary

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
)

if __name__ == "__main__":
    try:
        print("\n" + "="*60)
        print("BRANCH PERFORMANCE ANALYSIS")
        print("="*60)
        
        perf_df = analyze_branch_performance()
        print_branch_performance_summary(perf_df)
        
        print("\n✓ Branch performance analysis completed!")
        print(f"Report saved to: data/processed/branch_performance.csv")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
