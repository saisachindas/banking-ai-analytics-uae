"""
Database Connection Layer

This module provides SQLAlchemy ORM setup, session management, and database
utilities for the Banking AI Analytics platform.
"""

import os
from typing import Generator
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Database URL from environment or default to SQLite
DB_URL = os.getenv(
    "DB_URL",
    "sqlite:///./uae_banking.db"
)

logger.info(f"Database URL: {DB_URL}")

# Create SQLAlchemy engine
if "sqlite" in DB_URL:
    # SQLite-specific configuration for local development
    engine = create_engine(
        DB_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=os.getenv("DB_ECHO", "false").lower() == "true"
    )
    logger.info("Using SQLite database for local development")
else:
    # PostgreSQL configuration for production
    engine = create_engine(
        DB_URL,
        pool_size=int(os.getenv("DB_POOL_SIZE", 10)),
        max_overflow=int(os.getenv("DB_MAX_OVERFLOW", 20)),
        echo=os.getenv("DB_ECHO", "false").lower() == "true"
    )
    logger.info("Using PostgreSQL database for production")

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting database sessions.
    Yields a database session and ensures it's closed after use.
    
    Usage:
        db = next(get_db())
        # use db
        db.close()
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection() -> bool:
    """
    Test database connectivity.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.info("Database connection successful")
            return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


def get_table_count(table_name: str) -> int:
    """
    Get row count for a specific table.
    
    Args:
        table_name: Name of the table
    
    Returns:
        int: Number of rows in the table
    """
    db = SessionLocal()
    try:
        result = db.execute(text(f"SELECT COUNT(*) as cnt FROM {table_name}"))
        count = result.scalar()
        logger.info(f"Table {table_name} has {count} rows")
        return count
    except Exception as e:
        logger.error(f"Error getting count for {table_name}: {e}")
        return 0
    finally:
        db.close()


def get_database_info() -> dict:
    """
    Get information about the database schema.
    
    Returns:
        dict: Dictionary containing tables and their column information
    """
    inspector = inspect(engine)
    db_info = {}
    
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        db_info[table_name] = {
            "columns": [col["name"] for col in columns],
            "row_count": get_table_count(table_name)
        }
    
    return db_info


if __name__ == "__main__":
    # Test connection and display database info
    if test_connection():
        logger.info("\n=== Database Information ===")
        db_info = get_database_info()
        for table_name, info in db_info.items():
            logger.info(f"\nTable: {table_name}")
            logger.info(f"  Columns: {', '.join(info['columns'])}")
            logger.info(f"  Rows: {info['row_count']}")
    else:
        logger.error("Failed to connect to database")
