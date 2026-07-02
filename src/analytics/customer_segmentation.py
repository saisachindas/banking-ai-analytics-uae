"""
Customer Segmentation Module

Implements RFM (Recency, Frequency, Monetary) analysis and K-Means clustering
to segment customers into meaningful groups for targeted marketing and risk management.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sqlalchemy import text
import logging
from src.db.connection import SessionLocal

logger = logging.getLogger(__name__)


def compute_rfm_segments(
    snapshot_date: datetime = None,
    n_clusters: int = 4,
    output_path: str = "data/processed/customer_segments.csv"
) -> pd.DataFrame:
    """
    Compute RFM (Recency, Frequency, Monetary) segmentation for all customers.
    
    Args:
        snapshot_date: Date for RFM calculation (defaults to today)
        n_clusters: Number of K-Means clusters (default 4)
        output_path: Path to save segmentation results
    
    Returns:
        pd.DataFrame: Customer segments with RFM scores and cluster assignments
    
    Examples:
        segments = compute_rfm_segments(n_clusters=4)
        segments = compute_rfm_segments(
            snapshot_date=datetime(2024, 6, 30),
            n_clusters=3
        )
    """
    if snapshot_date is None:
        snapshot_date = datetime.now()
    
    logger.info(f"Computing RFM segmentation as of {snapshot_date}")
    
    db = SessionLocal()
    try:
        # Query customer transaction data
        query = text("""
            SELECT 
                c.customer_id,
                c.customer_name,
                c.customer_segment,
                COUNT(DISTINCT t.transaction_id) as transaction_count,
                MAX(t.transaction_date) as last_transaction_date,
                SUM(CASE WHEN t.transaction_type = 'Debit' THEN t.transaction_amount_aed ELSE 0 END) as total_debits
            FROM CUSTOMERS c
            LEFT JOIN TRANSACTIONS t ON c.customer_id = t.customer_id
            WHERE c.account_status = 'Active'
            GROUP BY c.customer_id, c.customer_name, c.customer_segment
        """)
        
        df = pd.read_sql(query, db.bind)
        logger.info(f"Retrieved data for {len(df)} customers")
        
        # Calculate RFM metrics
        df['recency_days'] = df['last_transaction_date'].apply(
            lambda x: (snapshot_date.date() - x).days if pd.notna(x) else 999
        )
        df['frequency'] = df['transaction_count']
        df['monetary'] = df['total_debits'].fillna(0)
        
        # Create RFM DataFrame
        rfm = df[['customer_id', 'customer_name', 'customer_segment', 'recency_days', 'frequency', 'monetary']].copy()
        
        # Standardize features for clustering
        scaler = StandardScaler()
        rfm_scaled = scaler.fit_transform(rfm[['recency_days', 'frequency', 'monetary']])
        
        # Apply K-Means clustering
        logger.info(f"Applying K-Means clustering with {n_clusters} clusters")
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        rfm['cluster'] = kmeans.fit_predict(rfm_scaled)
        
        # Map clusters to segment names
        segment_names = {
            0: "Segment A",
            1: "Segment B",
            2: "Segment C",
            3: "Segment D"
        }
        rfm['segment_name'] = rfm['cluster'].map(segment_names)
        
        # Calculate RFM scores (1-5 scale)
        rfm['recency_score'] = pd.qcut(rfm['recency_days'], q=5, labels=[5, 4, 3, 2, 1], duplicates='drop')
        rfm['frequency_score'] = pd.qcut(rfm['frequency'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')
        rfm['monetary_score'] = pd.qcut(rfm['monetary'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')
        rfm['rfm_score'] = rfm['recency_score'].astype(int) + rfm['frequency_score'].astype(int) + rfm['monetary_score'].astype(int)
        
        # Save to CSV
        rfm.to_csv(output_path, index=False)
        logger.info(f"Segmentation results saved to {output_path}")
        
        return rfm
    
    except Exception as e:
        logger.error(f"Error in RFM segmentation: {e}")
        raise
    finally:
        db.close()


def print_segment_stats(segments: pd.DataFrame) -> None:
    """
    Print summary statistics for customer segments.
    
    Args:
        segments: DataFrame with segment assignments
    """
    print("\n=== Customer Segmentation Statistics ===")
    print(f"Total customers: {len(segments)}")
    print(f"\nSegment Distribution:")
    print(segments['segment_name'].value_counts().sort_index())
    
    print(f"\nRFM Score Distribution:")
    print(segments['rfm_score'].describe())
    
    print(f"\nSegment Characteristics:")
    for segment in segments['segment_name'].unique():
        seg_data = segments[segments['segment_name'] == segment]
        print(f"\n{segment}:")
        print(f"  Count: {len(seg_data)}")
        print(f"  Avg Recency: {seg_data['recency_days'].mean():.1f} days")
        print(f"  Avg Frequency: {seg_data['frequency'].mean():.1f} transactions")
        print(f"  Avg Monetary: AED {seg_data['monetary'].mean():,.2f}")
        print(f"  Avg RFM Score: {seg_data['rfm_score'].mean():.1f}")


if __name__ == "__main__":
    # Run customer segmentation
    segments = compute_rfm_segments(n_clusters=4)
    print_segment_stats(segments)
