"""
Generative AI - Complaint Summary Generator

Uses HuggingFace models to generate concise complaint summaries and
suggested resolution notes for customer support teams.
"""

import pandas as pd
from transformers import pipeline
from sqlalchemy import text
import logging
import os
from src.db.connection import SessionLocal

logger = logging.getLogger(__name__)

# Load summarization pipeline
try:
    summarizer = pipeline(
        "summarization",
        model="facebook/bart-large-cnn",
        device=0 if True else -1
    )
    logger.info("Loaded BART model for complaint summarization")
except Exception as e:
    logger.warning(f"Could not load BART model: {e}. Using fallback.")
    summarizer = pipeline(
        "text2text-generation",
        model="google/flan-t5-base",
        device=-1
    )


def generate_complaint_summaries(
    output_path: str = "data/processed/complaint_summaries.csv"
) -> pd.DataFrame:
    """
    Generate AI-powered summaries for open complaints.
    
    Args:
        output_path: Path to save complaint summaries
    
    Returns:
        pd.DataFrame: Complaints with AI-generated summaries
    """
    logger.info("Generating complaint summaries...")
    
    db = SessionLocal()
    try:
        # Query open complaints
        query = text("""
            SELECT 
                c.complaint_id,
                c.customer_id,
                c.complaint_category,
                c.complaint_type,
                c.complaint_description,
                c.severity,
                c.complaint_date,
                c.status,
                cust.customer_name,
                b.branch_name
            FROM COMPLAINTS c
            JOIN CUSTOMERS cust ON c.customer_id = cust.customer_id
            JOIN BRANCHES b ON c.branch_id = b.branch_id
            WHERE c.status IN ('Open', 'In Progress')
            ORDER BY c.complaint_date DESC
        """)
        
        df = pd.read_sql(query, db.bind)
        logger.info(f"Retrieved {len(df)} open complaints")
        
        # Generate summaries
        summaries = []
        resolutions = []
        
        for idx, row in df.iterrows():
            try:
                # Generate summary
                summary_prompt = f"Summarize this banking complaint in 2 sentences: {row['complaint_description']}"
                summary_result = summarizer(summary_prompt, max_length=100, do_sample=False)
                summary = summary_result[0]['generated_text'] if isinstance(summary_result, list) else summary_result
                summaries.append(summary)
                
                # Generate resolution suggestion
                resolution_prompt = f"Suggest a resolution for this {row['complaint_category']} complaint: {row['complaint_description']}"
                resolution_result = summarizer(resolution_prompt, max_length=150, do_sample=False)
                resolution = resolution_result[0]['generated_text'] if isinstance(resolution_result, list) else resolution_result
                resolutions.append(resolution)
                
            except Exception as e:
                logger.warning(f"Error generating summary for complaint {row['complaint_id']}: {e}")
                summaries.append(row['complaint_description'][:100] + "...")
                resolutions.append("Manual review required")
        
        df['ai_summary'] = summaries
        df['suggested_resolution'] = resolutions
        
        # Save to CSV
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        df.to_csv(output_path, index=False)
        logger.info(f"Complaint summaries saved to {output_path}")
        
        return df
    
    except Exception as e:
        logger.error(f"Error generating complaint summaries: {e}")
        raise
    finally:
        db.close()


def print_complaint_summaries(df: pd.DataFrame, limit: int = 5) -> None:
    """
    Print complaint summaries in a readable format.
    
    Args:
        df: Complaint summaries DataFrame
        limit: Number of complaints to display
    """
    print("\n=== Recent Complaint Summaries ===")
    print(f"Total open complaints: {len(df)}")
    
    for idx, row in df.head(limit).iterrows():
        print(f"\nComplaint #{row['complaint_id']}")
        print(f"  Customer: {row['customer_name']}")
        print(f"  Category: {row['complaint_category']}")
        print(f"  Severity: {row['severity']}")
        print(f"  Summary: {row['ai_summary']}")
        print(f"  Suggested Resolution: {row['suggested_resolution']}")


if __name__ == "__main__":
    # Generate complaint summaries
    complaint_df = generate_complaint_summaries()
    print_complaint_summaries(complaint_df, limit=3)
