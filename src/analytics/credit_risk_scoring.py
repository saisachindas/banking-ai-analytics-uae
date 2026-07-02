"""
Credit Risk Scoring Module

Implements logistic regression model to predict Non-Performing Loans (NPL)
and assess customer credit risk based on loan and customer attributes.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix, roc_curve
from sqlalchemy import text
import logging
import pickle
from src.db.connection import SessionLocal

logger = logging.getLogger(__name__)


def build_credit_risk_model(
    test_size: float = 0.2,
    model_path: str = "models/credit_risk_model.pkl",
    scaler_path: str = "models/credit_risk_scaler.pkl"
) -> tuple:
    """
    Build and train a logistic regression model to predict NPL (Non-Performing Loans).
    
    Args:
        test_size: Proportion of data to use for testing (default 0.2)
        model_path: Path to save trained model
        scaler_path: Path to save fitted scaler
    
    Returns:
        tuple: (trained_model, scaler, metrics_dict)
    
    Examples:
        model, scaler, metrics = build_credit_risk_model()
        model, scaler, metrics = build_credit_risk_model(test_size=0.3)
    """
    logger.info("Building credit risk model...")
    
    db = SessionLocal()
    try:
        # Query loan data with features
        query = text("""
            SELECT 
                l.loan_id,
                l.customer_id,
                l.loan_amount_aed,
                l.outstanding_balance_aed,
                l.interest_rate_per_annum,
                l.loan_term_months,
                l.days_overdue,
                l.npl_flag,
                c.annual_income_aed,
                c.aml_risk_score,
                c.kyc_status,
                rf.risk_score as customer_risk_score
            FROM LOANS l
            JOIN CUSTOMERS c ON l.customer_id = c.customer_id
            LEFT JOIN RISK_FACTORS rf ON c.customer_id = rf.customer_id AND rf.risk_type = 'Credit Risk'
            WHERE l.loan_status IN ('Active', 'Default', 'Closed')
        """)
        
        df = pd.read_sql(query, db.bind)
        logger.info(f"Retrieved {len(df)} loan records")
        
        # Feature engineering
        df['loan_to_income'] = df['loan_amount_aed'] / (df['annual_income_aed'].fillna(1) + 1)
        df['debt_to_income'] = df['outstanding_balance_aed'] / (df['annual_income_aed'].fillna(1) + 1)
        df['kyc_verified'] = (df['kyc_status'] == 'Verified').astype(int)
        df['has_risk_score'] = df['customer_risk_score'].notna().astype(int)
        df['risk_score'] = df['customer_risk_score'].fillna(50)
        
        # Drop rows with missing target
        df = df.dropna(subset=['npl_flag'])
        
        # Feature selection
        features = ['loan_amount_aed', 'outstanding_balance_aed', 'interest_rate_per_annum',
                   'loan_term_months', 'days_overdue', 'aml_risk_score', 'loan_to_income',
                   'debt_to_income', 'kyc_verified', 'risk_score']
        
        X = df[features].fillna(0)
        y = df['npl_flag'].astype(int)
        
        logger.info(f"Feature matrix shape: {X.shape}")
        logger.info(f"Target distribution: {y.value_counts().to_dict()}")
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train logistic regression model
        logger.info("Training logistic regression model...")
        model = LogisticRegression(max_iter=1000, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        train_score = model.score(X_train_scaled, y_train)
        test_score = model.score(X_test_scaled, y_test)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        
        logger.info(f"Training accuracy: {train_score:.4f}")
        logger.info(f"Testing accuracy: {test_score:.4f}")
        logger.info(f"ROC-AUC Score: {roc_auc:.4f}")
        
        y_pred = model.predict(X_test_scaled)
        logger.info(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")
        
        # Save model and scaler
        import os
        os.makedirs(os.path.dirname(model_path) or ".", exist_ok=True)
        
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        logger.info(f"Model saved to {model_path}")
        
        with open(scaler_path, 'wb') as f:
            pickle.dump(scaler, f)
        logger.info(f"Scaler saved to {scaler_path}")
        
        metrics = {
            "train_accuracy": train_score,
            "test_accuracy": test_score,
            "roc_auc": roc_auc,
            "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
            "feature_importance": dict(zip(features, model.coef_[0]))
        }
        
        return model, scaler, metrics
    
    except Exception as e:
        logger.error(f"Error building credit risk model: {e}")
        raise
    finally:
        db.close()


def predict_npl_risk(
    loan_data: dict,
    model_path: str = "models/credit_risk_model.pkl",
    scaler_path: str = "models/credit_risk_scaler.pkl"
) -> float:
    """
    Predict NPL probability for a single loan.
    
    Args:
        loan_data: Dictionary with loan features
        model_path: Path to trained model
        scaler_path: Path to fitted scaler
    
    Returns:
        float: Predicted NPL probability (0-1)
    """
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        
        features = ['loan_amount_aed', 'outstanding_balance_aed', 'interest_rate_per_annum',
                   'loan_term_months', 'days_overdue', 'aml_risk_score', 'loan_to_income',
                   'debt_to_income', 'kyc_verified', 'risk_score']
        
        feature_vector = np.array([loan_data.get(f, 0) for f in features]).reshape(1, -1)
        feature_vector_scaled = scaler.transform(feature_vector)
        probability = model.predict_proba(feature_vector_scaled)[0, 1]
        
        return probability
    
    except Exception as e:
        logger.error(f"Error predicting NPL risk: {e}")
        return 0.5


if __name__ == "__main__":
    # Build and evaluate credit risk model
    model, scaler, metrics = build_credit_risk_model()
    print("\n=== Credit Risk Model Metrics ===")
    print(f"Training Accuracy: {metrics['train_accuracy']:.4f}")
    print(f"Testing Accuracy: {metrics['test_accuracy']:.4f}")
    print(f"ROC-AUC Score: {metrics['roc_auc']:.4f}")
    print(f"\nConfusion Matrix:\n{metrics['confusion_matrix']}")
