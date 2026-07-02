"""
Digital Channel Analytics Module

Analyzes customer interactions across digital channels (mobile app, web portal, SMS)
to understand usage patterns, identify drop-off points, and optimize digital experiences.
"""

import pandas as pd
from sqlalchemy import text
import logging
from src.db.connection import SessionLocal

logger = logging.getLogger(__name__)


def analyze_digital_channels(
    output_path: str = "data/processed/digital_channel_kpis.csv"
) -> pd.DataFrame:
    """
    Analyze digital channel usage and performance metrics.
    
    Args:
        output_path: Path to save digital channel KPIs
    
    Returns:
        pd.DataFrame: Digital channel analytics
    """
    logger.info("Analyzing digital channel analytics...")
    
    db = SessionLocal()
    try:
        # Query digital channel events
        query = text("""
            SELECT 
                channel,
                event_type,
                COUNT(DISTINCT session_id) as sessions,
                COUNT(DISTINCT customer_id) as unique_customers,
                COUNT(*) as total_events,
                AVG(session_duration_seconds) as avg_session_duration,
                AVG(page_views) as avg_page_views,
                SUM(CASE WHEN transaction_value_aed > 0 THEN transaction_value_aed ELSE 0 END) as transaction_value,
                SUM(CASE WHEN success_flag = TRUE THEN 1 ELSE 0 END) as successful_events,
                SUM(CASE WHEN success_flag = FALSE THEN 1 ELSE 0 END) as failed_events
            FROM DIGITAL_CHANNEL_EVENTS
            GROUP BY channel, event_type
        """)
        
        df = pd.read_sql(query, db.bind)
        logger.info(f"Retrieved data for {len(df)} channel-event combinations")
        
        # Calculate KPIs
        df['success_rate'] = df['successful_events'] / (df['total_events'].fillna(1) + 1)
        df['avg_transaction_value'] = df['transaction_value'] / (df['successful_events'].fillna(1) + 1)
        df['engagement_score'] = (df['sessions'] / df['unique_customers'].fillna(1)) * df['success_rate']
        
        # Save analytics
        df.to_csv(output_path, index=False)
        logger.info(f"Digital channel KPIs saved to {output_path}")
        
        return df
    
    except Exception as e:
        logger.error(f"Error in digital channel analysis: {e}")
        raise
    finally:
        db.close()


def analyze_device_preferences() -> pd.DataFrame:
    """
    Analyze customer device preferences and usage patterns.
    
    Returns:
        pd.DataFrame: Device usage statistics
    """
    logger.info("Analyzing device preferences...")
    
    db = SessionLocal()
    try:
        query = text("""
            SELECT 
                device_type,
                COUNT(*) as total_events,
                COUNT(DISTINCT customer_id) as unique_users,
                COUNT(DISTINCT session_id) as sessions,
                AVG(session_duration_seconds) as avg_session_duration,
                SUM(CASE WHEN success_flag = TRUE THEN 1 ELSE 0 END) as successful_events
            FROM DIGITAL_CHANNEL_EVENTS
            GROUP BY device_type
            ORDER BY total_events DESC
        """)
        
        df = pd.read_sql(query, db.bind)
        df['success_rate'] = df['successful_events'] / df['total_events']
        return df
    
    except Exception as e:
        logger.error(f"Error analyzing device preferences: {e}")
        raise
    finally:
        db.close()


def print_digital_analytics_summary(df: pd.DataFrame) -> None:
    """
    Print summary of digital channel analytics.
    
    Args:
        df: Digital channel analytics DataFrame
    """
    print("\n=== Digital Channel Analytics Summary ===")
    print(f"\nChannel Performance:")
    channel_stats = df.groupby('channel').agg({
        'total_events': 'sum',
        'unique_customers': 'sum',
        'success_rate': 'mean',
        'engagement_score': 'mean'
    }).round(4)
    print(channel_stats)
    
    print(f"\nDevice Preferences:")
    device_df = analyze_device_preferences()
    print(device_df.to_string(index=False))
    
    print(f"\nTop Event Types:")
    top_events = df.nlargest(5, 'total_events')[['channel', 'event_type', 'total_events', 'success_rate']]
    print(top_events.to_string(index=False))


if __name__ == "__main__":
    # Analyze digital channels
    analytics_df = analyze_digital_channels()
    print_digital_analytics_summary(analytics_df)
