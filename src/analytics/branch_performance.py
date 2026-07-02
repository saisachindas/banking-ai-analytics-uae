"""
Branch Performance Analytics Module

Analyzes branch-level performance metrics including revenue, transaction volume,
and customer satisfaction to identify high-performing and underperforming branches.
"""

import pandas as pd
from sqlalchemy import text
import logging
from src.db.connection import SessionLocal

logger = logging.getLogger(__name__)


def analyze_branch_performance(
    output_path: str = "data/processed/branch_performance.csv"
) -> pd.DataFrame:
    """
    Analyze key performance indicators for all branches.
    
    Args:
        output_path: Path to save branch performance report
    
    Returns:
        pd.DataFrame: Branch performance metrics
    """
    logger.info("Analyzing branch performance...")
    
    db = SessionLocal()
    try:
        # Query branch performance data
        query = text("""
            SELECT 
                b.branch_id,
                b.branch_name,
                b.emirate,
                b.city,
                b.staff_count,
                COUNT(DISTINCT a.account_id) as total_accounts,
                COUNT(DISTINCT a.customer_id) as total_customers,
                COUNT(DISTINCT t.transaction_id) as total_transactions,
                SUM(CASE WHEN t.transaction_type = 'Debit' THEN t.transaction_amount_aed ELSE 0 END) as total_debits,
                SUM(CASE WHEN t.transaction_type = 'Credit' THEN t.transaction_amount_aed ELSE 0 END) as total_credits,
                AVG(a.current_balance_aed) as avg_balance,
                COUNT(DISTINCT l.loan_id) as total_loans,
                SUM(l.outstanding_balance_aed) as total_loan_portfolio,
                COUNT(DISTINCT CASE WHEN c.status = 'Resolved' THEN c.complaint_id END) as resolved_complaints,
                COUNT(DISTINCT CASE WHEN c.status = 'Open' THEN c.complaint_id END) as open_complaints
            FROM BRANCHES b
            LEFT JOIN ACCOUNTS a ON b.branch_id = a.branch_id
            LEFT JOIN TRANSACTIONS t ON a.account_id = t.account_id
            LEFT JOIN LOANS l ON b.branch_id = l.branch_id
            LEFT JOIN COMPLAINTS c ON b.branch_id = c.branch_id
            GROUP BY b.branch_id, b.branch_name, b.emirate, b.city, b.staff_count
        """)
        
        df = pd.read_sql(query, db.bind)
        logger.info(f"Retrieved performance data for {len(df)} branches")
        
        # Calculate KPIs
        df['revenue_per_head'] = df['total_debits'] / (df['staff_count'].fillna(1) + 1)
        df['txns_per_customer'] = df['total_transactions'] / (df['total_customers'].fillna(1) + 1)
        df['accounts_per_customer'] = df['total_accounts'] / (df['total_customers'].fillna(1) + 1)
        df['loan_to_deposit_ratio'] = df['total_loan_portfolio'] / (df['total_debits'].fillna(1) + 1)
        df['complaint_resolution_rate'] = df['resolved_complaints'] / (df['resolved_complaints'] + df['open_complaints'].fillna(1) + 1)
        df['avg_transaction_size'] = df['total_debits'] / (df['total_transactions'].fillna(1) + 1)
        
        # Save performance report
        df.to_csv(output_path, index=False)
        logger.info(f"Branch performance report saved to {output_path}")
        
        return df
    
    except Exception as e:
        logger.error(f"Error in branch performance analysis: {e}")
        raise
    finally:
        db.close()


def print_branch_performance_summary(df: pd.DataFrame) -> None:
    """
    Print summary of branch performance metrics.
    
    Args:
        df: Branch performance DataFrame
    """
    print("\n=== Branch Performance Summary ===")
    print(f"Total branches: {len(df)}")
    
    print(f"\nTop 5 branches by revenue per head:")
    top_revenue = df.nlargest(5, 'revenue_per_head')[['branch_name', 'emirate', 'revenue_per_head', 'staff_count']]
    print(top_revenue.to_string(index=False))
    
    print(f"\nTop 5 branches by transaction volume:")
    top_txns = df.nlargest(5, 'total_transactions')[['branch_name', 'emirate', 'total_transactions', 'total_customers']]
    print(top_txns.to_string(index=False))
    
    print(f"\nTop 5 branches by customer satisfaction (complaint resolution):")
    top_satisfaction = df.nlargest(5, 'complaint_resolution_rate')[['branch_name', 'emirate', 'complaint_resolution_rate']]
    print(top_satisfaction.to_string(index=False))
    
    print(f"\nKey Metrics Summary:")
    print(f"  Avg revenue per head: AED {df['revenue_per_head'].mean():,.2f}")
    print(f"  Avg transactions per customer: {df['txns_per_customer'].mean():.2f}")
    print(f"  Avg complaint resolution rate: {df['complaint_resolution_rate'].mean():.2%}")


if __name__ == "__main__":
    # Analyze branch performance
    perf_df = analyze_branch_performance()
    print_branch_performance_summary(perf_df)
