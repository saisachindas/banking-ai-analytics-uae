#!/usr/bin/env python
"""
Run Credit Risk Scoring Model
"""

import sys
import logging
from src.analytics.credit_risk_scoring import build_credit_risk_model

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
)

if __name__ == "__main__":
    try:
        print("\n" + "="*60)
        print("CREDIT RISK SCORING MODEL")
        print("="*60)
        
        model, scaler, metrics = build_credit_risk_model(test_size=0.2)
        
        print("\n" + "="*60)
        print("MODEL PERFORMANCE METRICS")
        print("="*60)
        print(f"Training Accuracy:  {metrics['train_accuracy']:.4f}")
        print(f"Testing Accuracy:   {metrics['test_accuracy']:.4f}")
        print(f"ROC-AUC Score:      {metrics['roc_auc']:.4f}")
        
        print(f"\n✓ Credit risk model trained successfully!")
        print(f"Model saved to: models/credit_risk_model.pkl")
        print(f"Scaler saved to: models/credit_risk_scaler.pkl")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
