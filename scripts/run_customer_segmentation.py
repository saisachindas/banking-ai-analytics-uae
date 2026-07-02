#!/usr/bin/env python
"""
Run Customer Segmentation Analysis
"""

import sys
import logging
from src.analytics.customer_segmentation import compute_rfm_segments, print_segment_stats

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
)

if __name__ == "__main__":
    try:
        print("\n" + "="*60)
        print("CUSTOMER SEGMENTATION ANALYSIS")
        print("="*60)
        
        segments = compute_rfm_segments(n_clusters=4)
        print_segment_stats(segments)
        
        print("\n✓ Customer segmentation completed successfully!")
        print(f"Results saved to: data/processed/customer_segments.csv")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
