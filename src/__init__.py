"""
Banking AI Analytics Platform - Main Package
"""

__version__ = "1.0.0"
__author__ = "Banking AI Team"
__description__ = "Production-ready AI platform for UAE banking analytics"

from src import db, analytics, genai, agents

__all__ = [
    "db",
    "analytics",
    "genai",
    "agents"
]
