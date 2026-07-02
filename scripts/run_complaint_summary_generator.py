#!/usr/bin/env python
"""
Run Complaint Summary Generation
"""

import sys
import logging
from src.genai.complaint_summary_generator import generate_complaint_summaries, print_complaint_summaries

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
)

if __name__ == "__main__":
    try:
        print("\n" + "="*60)
        print("COMPLAINT SUMMARY GENERATION")
        print("="*60)
        
        complaints_df = generate_complaint_summaries()
        print_complaint_summaries(complaints_df, limit=3)
        
        print("\n✓ Complaint summaries generated successfully!")
        print(f"Summaries saved to: data/processed/complaint_summaries.csv")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
