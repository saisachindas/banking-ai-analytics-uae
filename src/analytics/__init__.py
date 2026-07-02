"""
Package initialization for analytics module.
"""

from .customer_segmentation import compute_rfm_segments
from .credit_risk_scoring import build_credit_risk_model
from .fraud_detection import detect_fraud_anomalies
from .branch_performance import analyze_branch_performance
from .digital_channel_analytics import analyze_digital_channels
from .product_profitability import analyze_product_profitability

__all__ = [
    "compute_rfm_segments",
    "build_credit_risk_model",
    "detect_fraud_anomalies",
    "analyze_branch_performance",
    "analyze_digital_channels",
    "analyze_product_profitability"
]
