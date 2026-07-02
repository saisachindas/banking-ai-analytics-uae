#!/usr/bin/env python
"""
Run Digital Channel Analytics
"""

import sys
import logging
from src.analytics.digital_channel_analytics import analyze_digital_channels, print_digital_analytics_summary

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
)

if __name__ == "__main__":
    try:
        print("\n" + "="*60)
        print("DIGITAL CHANNEL ANALYTICS")
        print("="*60)
        
        analytics_df = analyze_digital_channels()
        print_digital_analytics_summary(analytics_df)
        
        print("\n✓ Digital channel analytics completed!")
        print(f"KPIs saved to: data/processed/digital_channel_kpis.csv")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
