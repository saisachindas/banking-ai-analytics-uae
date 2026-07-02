#!/usr/bin/env python
"""
Run Fraud Detection Analysis
"""

import sys
import logging
from src.analytics.fraud_detection import detect_fraud_anomalies, print_fraud_stats

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
)

if __name__ == "__main__":
    try:
        print("\n" + "="*60)
        print("FRAUD DETECTION ANALYSIS")
        print("="*60)
        
        alerts = detect_fraud_anomalies(
            lookback_days=90,
            contamination=0.05
        )
        print_fraud_stats(alerts)
        
        print("\n✓ Fraud detection completed successfully!")
        print(f"Alerts saved to: data/processed/fraud_alerts.csv")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
