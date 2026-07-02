"""
Fraud Detection Module

Implements Isolation Forest anomaly detection to identify suspicious transactions
based on behavioral patterns and transaction characteristics.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
from sqlalchemy import text
import logging
from src.db.connection import SessionLocal

logger = logging.getLogger(__name__)


def detect_fraud_anomalies(
    lookback_days: int = 90,
    contamination: float = 0.05,
    output_path: str = "data/processed/fraud_alerts.csv"
) -> pd.DataFrame:
    """
    Detect fraudulent transactions using Isolation Forest anomaly detection.
    
    Args:
        lookback_days: Number of days to analyze (default 90)
        contamination: Expected proportion of outliers (default 0.05)
        output_path: Path to save fraud alerts
    
    Returns:
        pd.DataFrame: Flagged suspicious transactions
    
    Examples:
        fraud_alerts = detect_fraud_anomalies(lookback_days=90)
        fraud_alerts = detect_fraud_anomalies(contamination=0.03)
    """
    logger.info(f"Detecting fraud anomalies for last {lookback_days} days")
    
    db = SessionLocal()
    try:
        cutoff_date = (datetime.now() - timedelta(days=lookback_days)).date()
        
        # Query recent transactions
        query = text(f"""
            SELECT 
                t.transaction_id,
                t.account_id,
                t.customer_id,
                t.transaction_date,
                t.transaction_time,
                t.transaction_amount_aed,
                t.transaction_type,
                t.channel,
                c.annual_income_aed,
                a.current_balance_aed
            FROM TRANSACTIONS t
            JOIN CUSTOMERS c ON t.customer_id = c.customer_id
            JOIN ACCOUNTS a ON t.account_id = a.account_id
            WHERE t.transaction_date >= '{cutoff_date}'
            AND t.status = 'Completed'
        """)
        
        df = pd.read_sql(query, db.bind)
        logger.info(f"Retrieved {len(df)} transactions from last {lookback_days} days")
        
        # Feature engineering
        df['hour'] = pd.to_datetime(df['transaction_time']).dt.hour
        df['is_weekend'] = pd.to_datetime(df['transaction_date']).dt.dayofweek.isin([5, 6]).astype(int)
        df['is_night'] = df['hour'].isin([0, 1, 2, 3, 4, 5]).astype(int)
        df['is_large_amount'] = (df['transaction_amount_aed'] > df['annual_income_aed'] * 0.1).astype(int)
        df['channel_encoded'] = pd.factorize(df['channel'])[0]
        df['transaction_type_encoded'] = pd.factorize(df['transaction_type'])[0]
        
        # Feature selection
        features = ['transaction_amount_aed', 'hour', 'is_weekend', 'is_night', 
                   'is_large_amount', 'channel_encoded', 'transaction_type_encoded']
        
        X = df[features].fillna(0)
        
        # Apply Isolation Forest
        logger.info(f"Applying Isolation Forest with contamination={contamination}")
        iso_forest = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        
        df['anomaly_score'] = iso_forest.fit_predict(X)
        df['anomaly_proba'] = -iso_forest.score_samples(X)  # Higher = more anomalous
        
        # Flag fraudulent transactions
        df['fraud_flag'] = (df['anomaly_score'] == -1).astype(int)
        
        # Create alerts DataFrame
        alerts = df[df['fraud_flag'] == 1][[
            'transaction_id', 'customer_id', 'account_id', 'transaction_date',
            'transaction_time', 'transaction_amount_aed', 'channel',
            'anomaly_proba', 'is_night', 'is_weekend', 'is_large_amount'
        ]].copy()
        
        alerts = alerts.sort_values('anomaly_proba', ascending=False)
        logger.info(f"Detected {len(alerts)} suspicious transactions")
        
        # Save alerts
        alerts.to_csv(output_path, index=False)
        logger.info(f"Fraud alerts saved to {output_path}")
        
        return alerts
    
    except Exception as e:
        logger.error(f"Error in fraud detection: {e}")
        raise
    finally:
        db.close()


def print_fraud_stats(alerts: pd.DataFrame) -> None:
    """
    Print summary statistics for detected fraud alerts.
    
    Args:
        alerts: DataFrame with fraud alerts
    """
    print("\n=== Fraud Detection Statistics ===")
    print(f"Total suspicious transactions: {len(alerts)}")
    print(f"\nTop fraud indicators:")
    print(f"  Night transactions: {alerts['is_night'].sum()}")
    print(f"  Weekend transactions: {alerts['is_weekend'].sum()}")
    print(f"  Large amounts: {alerts['is_large_amount'].sum()}")
    
    print(f"\nTop 10 suspicious transactions:")
    print(alerts[['transaction_id', 'transaction_amount_aed', 'channel', 'anomaly_proba']].head(10))
    
    print(f"\nChannel distribution of frauds:")
    print(alerts['channel'].value_counts())


if __name__ == "__main__":
    # Run fraud detection
    alerts = detect_fraud_anomalies(lookback_days=90, contamination=0.05)
    print_fraud_stats(alerts)
