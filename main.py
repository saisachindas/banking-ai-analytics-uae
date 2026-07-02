#!/usr/bin/env python
"""
Banking AI Analytics Platform - Main Entry Point

This module initializes and orchestrates all platform components.
"""

import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/banking_ai.log')
    ]
)

logger = logging.getLogger(__name__)

# Ensure required directories exist
Paths = {
    'data_raw': Path('data/raw'),
    'data_processed': Path('data/processed'),
    'logs': Path('logs'),
    'models': Path('models')
}

for path_name, path in Paths.items():
    path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Ensured directory: {path}")


def initialize_platform():
    """
    Initialize the Banking AI Analytics Platform.
    """
    logger.info("\n" + "="*70)
    logger.info("BANKING AI ANALYTICS PLATFORM - INITIALIZATION")
    logger.info("="*70 + "\n")
    
    try:
        # Import and initialize components
        from src.db.connection import test_connection, get_database_info
        
        logger.info("Testing database connection...")
        if test_connection():
            logger.info("✓ Database connection successful")
            
            db_info = get_database_info()
            logger.info(f"✓ Database has {len(db_info)} tables")
            for table_name, info in db_info.items():
                logger.info(f"  - {table_name}: {info['row_count']} rows")
        else:
            logger.error("✗ Database connection failed")
            return False
        
        logger.info("\n" + "="*70)
        logger.info("PLATFORM INITIALIZED SUCCESSFULLY")
        logger.info("="*70)
        logger.info("\nAvailable modules:")
        logger.info("  - src.db: Database connection and utilities")
        logger.info("  - src.analytics: Analytics workflows (6 modules)")
        logger.info("  - src.genai: Generative AI (3 components)")
        logger.info("  - src.agents: Autonomous agents (3 agents)")
        logger.info("\nRun scripts/:")
        logger.info("  python scripts/run_customer_segmentation.py")
        logger.info("  python scripts/run_credit_risk_scoring.py")
        logger.info("  python scripts/run_fraud_detection.py")
        logger.info("  python scripts/run_branch_performance.py")
        logger.info("  python scripts/run_digital_channel_analytics.py")
        logger.info("  python scripts/run_product_profitability.py")
        logger.info("  python scripts/run_complaint_summary_generator.py")
        logger.info("  python scripts/run_customer_support_agent.py")
        logger.info("  python scripts/run_fraud_investigation_agent.py")
        logger.info("  python scripts/run_compliance_agent.py")
        logger.info("\n" + "="*70 + "\n")
        
        return True
    
    except Exception as e:
        logger.error(f"✗ Initialization failed: {e}")
        logger.exception(e)
        return False


if __name__ == "__main__":
    success = initialize_platform()
    sys.exit(0 if success else 1)
