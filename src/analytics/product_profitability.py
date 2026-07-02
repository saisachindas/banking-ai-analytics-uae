"""
Product Profitability Analysis Module

Analyzes profitability metrics for banking products including deposits, loans,
and cards to optimize product strategy and pricing.
"""

import pandas as pd
from sqlalchemy import text
import logging
from src.db.connection import SessionLocal

logger = logging.getLogger(__name__)


def analyze_product_profitability(
    output_path: str = "data/processed/product_profitability_report.csv"
) -> pd.DataFrame:
    """
    Analyze profitability metrics for all banking products.
    
    Args:
        output_path: Path to save product profitability report
    
    Returns:
        pd.DataFrame: Product profitability metrics
    """
    logger.info("Analyzing product profitability...")
    
    db = SessionLocal()
    try:
        # Query product data
        query = text("""
            SELECT 
                p.product_id,
                p.product_name,
                p.product_category,
                p.product_type,
                p.interest_rate_per_annum,
                p.annual_fee_aed,
                COUNT(DISTINCT a.account_id) as total_accounts,
                COUNT(DISTINCT a.customer_id) as total_customers,
                AVG(a.current_balance_aed) as avg_balance,
                SUM(a.current_balance_aed) as total_balance,
                COUNT(DISTINCT t.transaction_id) as total_transactions,
                SUM(CASE WHEN t.transaction_type = 'Debit' THEN t.transaction_amount_aed ELSE 0 END) as transaction_volume,
                COUNT(DISTINCT l.loan_id) as total_loans,
                SUM(l.outstanding_balance_aed) as total_loan_balance
            FROM PRODUCTS p
            LEFT JOIN ACCOUNTS a ON p.product_id = a.product_id
            LEFT JOIN TRANSACTIONS t ON a.account_id = t.account_id
            LEFT JOIN LOANS l ON p.product_id = l.product_id AND p.product_category = 'Loans'
            WHERE p.is_active = TRUE
            GROUP BY p.product_id, p.product_name, p.product_category, p.product_type,
                     p.interest_rate_per_annum, p.annual_fee_aed
        """)
        
        df = pd.read_sql(query, db.bind)
        logger.info(f"Retrieved profitability data for {len(df)} products")
        
        # Calculate profitability metrics
        # Interest income: (balance * interest rate)
        df['annual_interest_income'] = df['total_balance'].fillna(0) * (df['interest_rate_per_annum'] / 100)
        
        # Fee income: (accounts * annual fee)
        df['annual_fee_income'] = df['total_accounts'].fillna(0) * df['annual_fee_aed']
        
        # Total revenue
        df['total_annual_revenue'] = df['annual_interest_income'] + df['annual_fee_income']
        
        # Revenue per account
        df['revenue_per_account'] = df['total_annual_revenue'] / (df['total_accounts'].fillna(1) + 1)
        
        # Revenue per customer
        df['revenue_per_customer'] = df['total_annual_revenue'] / (df['total_customers'].fillna(1) + 1)
        
        # Transaction efficiency
        df['avg_transaction_value'] = df['transaction_volume'] / (df['total_transactions'].fillna(1) + 1)
        
        # Save report
        df.to_csv(output_path, index=False)
        logger.info(f"Product profitability report saved to {output_path}")
        
        return df
    
    except Exception as e:
        logger.error(f"Error in product profitability analysis: {e}")
        raise
    finally:
        db.close()


def print_product_profitability_summary(df: pd.DataFrame) -> None:
    """
    Print summary of product profitability metrics.
    
    Args:
        df: Product profitability DataFrame
    """
    print("\n=== Product Profitability Analysis ===")
    print(f"Total products: {len(df)}")
    
    print(f"\nTop 5 products by annual revenue:")
    top_revenue = df.nlargest(5, 'total_annual_revenue')[[
        'product_name', 'product_category', 'total_annual_revenue', 'total_accounts'
    ]]
    print(top_revenue.to_string(index=False))
    
    print(f"\nTop 5 products by revenue per account:")
    top_rpa = df.nlargest(5, 'revenue_per_account')[[
        'product_name', 'revenue_per_account', 'interest_rate_per_annum', 'annual_fee_aed'
    ]]
    print(top_rpa.to_string(index=False))
    
    print(f"\nProfitability by product category:")
    category_summary = df.groupby('product_category').agg({
        'total_annual_revenue': 'sum',
        'total_accounts': 'sum',
        'total_customers': 'sum',
        'revenue_per_account': 'mean'
    }).round(2)
    print(category_summary)
    
    print(f"\nKey Metrics:")
    print(f"  Total annual revenue: AED {df['total_annual_revenue'].sum():,.2f}")
    print(f"  Avg revenue per account: AED {df['revenue_per_account'].mean():,.2f}")
    print(f"  Avg revenue per customer: AED {df['revenue_per_customer'].mean():,.2f}")


if __name__ == "__main__":
    # Analyze product profitability
    prof_df = analyze_product_profitability()
    print_product_profitability_summary(prof_df)
