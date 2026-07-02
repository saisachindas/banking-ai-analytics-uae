"""
Generative AI - KYC Summary Generator

Uses HuggingFace Flan-T5 to generate concise, professional KYC summaries
for compliance officers from customer documents and risk assessment data.
"""

import pandas as pd
from transformers import pipeline
from sqlalchemy import text
import logging
from src.db.connection import SessionLocal

logger = logging.getLogger(__name__)

# Load text-to-text generation model
try:
    summarizer = pipeline(
        "text2text-generation",
        model="google/flan-t5-large",
        device=0 if True else -1  # Use GPU if available
    )
    logger.info("Loaded Flan-T5 model for KYC summarization")
except Exception as e:
    logger.warning(f"Could not load Flan-T5 model: {e}. Using CPU fallback.")
    summarizer = pipeline(
        "text2text-generation",
        model="google/flan-t5-base",
        device=-1  # CPU only
    )


def generate_kyc_summary(customer_id: int) -> dict:
    """
    Generate a professional KYC summary for a customer.
    
    Args:
        customer_id: ID of the customer
    
    Returns:
        dict: Summary details including text, risk flags, and recommendations
    
    Examples:
        summary = generate_kyc_summary(customer_id=1)
        print(summary['kyc_summary'])
    """
    logger.info(f"Generating KYC summary for customer {customer_id}")
    
    db = SessionLocal()
    try:
        # Query customer data
        query = text(f"""
            SELECT 
                c.customer_id,
                c.customer_name,
                c.nationality,
                c.employment_sector,
                c.annual_income_aed,
                c.kyc_status,
                c.pep_flag,
                c.sanctions_flag,
                c.aml_risk_score,
                STRING_AGG(DISTINCT kd.document_type, ', ') as documents,
                rf.risk_level,
                rf.risk_score
            FROM CUSTOMERS c
            LEFT JOIN KYC_DOCUMENTS kd ON c.customer_id = kd.customer_id AND kd.verification_status = 'Verified'
            LEFT JOIN RISK_FACTORS rf ON c.customer_id = rf.customer_id AND rf.risk_type = 'Compliance Risk'
            WHERE c.customer_id = {customer_id}
            GROUP BY c.customer_id, c.customer_name, c.nationality, c.employment_sector,
                     c.annual_income_aed, c.kyc_status, c.pep_flag, c.sanctions_flag,
                     c.aml_risk_score, rf.risk_level, rf.risk_score
        """)
        
        result = db.execute(query).fetchone()
        
        if not result:
            logger.error(f"Customer {customer_id} not found")
            return {"error": f"Customer {customer_id} not found"}
        
        customer_data = dict(result._mapping)
        
        # Build KYC context
        kyc_context = f"""
        Customer: {customer_data['customer_name']}
        Nationality: {customer_data['nationality']}
        Employment: {customer_data['employment_sector']}
        Annual Income: AED {customer_data['annual_income_aed']}
        KYC Status: {customer_data['kyc_status']}
        Documents Verified: {customer_data['documents']}
        PEP Flag: {customer_data['pep_flag']}
        Sanctions Flag: {customer_data['sanctions_flag']}
        AML Risk Score: {customer_data['aml_risk_score']}
        Risk Level: {customer_data['risk_level']}
        """
        
        # Generate summary using Flan-T5
        prompt = f"Summarize this KYC customer profile in 3 professional sentences for a compliance officer:\n{kyc_context}"
        
        summary_result = summarizer(prompt, max_length=150, do_sample=False)
        kyc_summary = summary_result[0]['generated_text']
        
        # Compile recommendations
        recommendations = []
        if customer_data['pep_flag']:
            recommendations.append("⚠️ PEP customer - Enhanced monitoring required")
        if customer_data['sanctions_flag']:
            recommendations.append("🚨 Sanctions flag - Immediate escalation required")
        if customer_data['aml_risk_score'] > 75:
            recommendations.append("⚠️ High AML risk - Monthly review recommended")
        if customer_data['kyc_status'] != 'Verified':
            recommendations.append("📋 KYC verification pending - Complete documentation required")
        if not recommendations:
            recommendations.append("✓ Low risk customer - Standard monitoring")
        
        return {
            "customer_id": customer_id,
            "customer_name": customer_data['customer_name'],
            "kyc_summary": kyc_summary,
            "recommendations": recommendations,
            "risk_level": customer_data['risk_level'],
            "aml_risk_score": customer_data['aml_risk_score']
        }
    
    except Exception as e:
        logger.error(f"Error generating KYC summary: {e}")
        return {"error": str(e)}
    finally:
        db.close()


if __name__ == "__main__":
    # Example: Generate KYC summary
    summary = generate_kyc_summary(customer_id=1)
    print("\n=== KYC Summary ===")
    if "error" not in summary:
        print(f"Customer: {summary['customer_name']}")
        print(f"\nSummary: {summary['kyc_summary']}")
        print(f"\nRecommendations:")
        for rec in summary['recommendations']:
            print(f"  {rec}")
        print(f"\nAML Risk Score: {summary['aml_risk_score']}/100")
    else:
        print(f"Error: {summary['error']}")
