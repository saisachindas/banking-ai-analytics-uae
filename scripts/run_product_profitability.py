#!/usr/bin/env python
"""
Run Product Profitability Analysis
"""

import sys
import logging
from src.analytics.product_profitability import analyze_product_profitability, print_product_profitability_summary

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
)

if __name__ == "__main__":
    try:
        print("\n" + "="*60)
        print("PRODUCT PROFITABILITY ANALYSIS")
        print("="*60)
        
        prof_df = analyze_product_profitability()
        print_product_profitability_summary(prof_df)
        
        print("\n✓ Product profitability analysis completed!")
        print(f"Report saved to: data/processed/product_profitability_report.csv")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
