# Banking AI Analytics Platform - Project Setup Guide

## 📋 Prerequisites

- **Python 3.9+** (check with `python --version`)
- **Git** (for cloning the repository)
- **PostgreSQL 12+** (for production) OR SQLite 3.0+ (for development)
- **8GB RAM minimum** (16GB recommended)
- **2GB free disk space** (for models and data)

## 🚀 Installation Steps

### Step 1: Clone Repository

```bash
git clone https://github.com/saisachindas/banking-ai-analytics-uae.git
cd banking-ai-analytics-uae
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate          # Linux/Mac
venv\Scripts\activate             # Windows
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Optional: Install development tools
pip install black flake8 pytest jupyter
```

### Step 4: Setup Environment Variables

```bash
# Copy example to .env
cp .env.example .env

# Edit .env (optional - defaults are fine for development)
vim .env  # or your preferred editor
```

### Step 5: Initialize Database

#### Option A: SQLite (Development - Recommended for quick start)

```bash
# Database will be created automatically on first run
# Or manually:
sqlite3 uae_banking.db < db/create_tables.sql
sqlite3 uae_banking.db < db/seed_data.sql

# Verify tables
sqlite3 uae_banking.db ".tables"
```

#### Option B: PostgreSQL (Production)

```bash
# Create database
creatdb -U postgres uae_banking

# Load schema
psql -U postgres -d uae_banking -f db/create_tables.sql

# Load sample data
psql -U postgres -d uae_banking -f db/seed_data.sql

# Set DB_URL in .env
export DB_URL=postgresql://postgres:password@localhost:5432/uae_banking
```

### Step 6: Initialize Platform

```bash
# Test database connection and initialize
python main.py

# Expected output:
# ✓ Database connection successful
# ✓ Database has 11 tables
# Platform initialized successfully
```

### Step 7: Run Your First Script

```bash
# Customer Segmentation
python scripts/run_customer_segmentation.py

# Credit Risk Scoring
python scripts/run_credit_risk_scoring.py

# Fraud Detection
python scripts/run_fraud_detection.py
```

## 🔍 Verification

### Check Installation

```bash
# Test imports
python -c "import pandas; import sklearn; import transformers; print('✓ All modules imported successfully')"

# Test database
python -c "from src.db.connection import test_connection; test_connection()"

# List available scripts
ls scripts/run_*.py
```

### First Run Checklist

- [ ] Python 3.9+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip list | grep pandas`)
- [ ] Database initialized
- [ ] Platform initialized (`python main.py`)
- [ ] At least one script runs successfully

## 📚 Usage Examples

### Run All Analytics

```bash
# Sequential execution
for script in scripts/run_*.py; do
    echo "Running $script..."
    python $script
done
```

### Run Specific Module

```bash
# Customer segmentation
python scripts/run_customer_segmentation.py

# Credit risk
python scripts/run_credit_risk_scoring.py

# Fraud detection
python scripts/run_fraud_detection.py

# Branch performance
python scripts/run_branch_performance.py

# Digital channels
python scripts/run_digital_channel_analytics.py

# Product profitability
python scripts/run_product_profitability.py

# Complaint summaries
python scripts/run_complaint_summary_generator.py

# Agents
python scripts/run_customer_support_agent.py
python scripts/run_fraud_investigation_agent.py
python scripts/run_compliance_agent.py
```

### Use in Python Code

```python
# Import and use modules
from src.analytics.customer_segmentation import compute_rfm_segments
from src.analytics.credit_risk_scoring import build_credit_risk_model
from src.analytics.fraud_detection import detect_fraud_anomalies
from src.agents.customer_support_agent import CustomerSupportAgent

# Customer Segmentation
segments = compute_rfm_segments(n_clusters=4)
print(f"Customers segmented into {segments['cluster'].nunique()} groups")

# Credit Risk Model
model, scaler, metrics = build_credit_risk_model()
print(f"Model ROC-AUC: {metrics['roc_auc']:.4f}")

# Fraud Detection
alerts = detect_fraud_anomalies(lookback_days=90)
print(f"Found {len(alerts)} suspicious transactions")

# Customer Support Agent
agent = CustomerSupportAgent()
response = agent.handle_request(1, "What is my balance?")
print(response)
```

## 🔧 Troubleshooting

### Database Connection Error

```bash
# Check if SQLite file exists
ls -la uae_banking.db

# Or test PostgreSQL
psql -U postgres -d uae_banking -c "SELECT 1"

# Verify connection string in .env
cat .env | grep DB_URL
```

### Import Error

```bash
# Reinstall requirements
pip install --force-reinstall -r requirements.txt

# Verify installation
python -c "import sklearn; print(sklearn.__version__)"
```

### Model Download Error

```bash
# Pre-download HuggingFace models
python -c "from transformers import AutoModel; AutoModel.from_pretrained('google/flan-t5-base')"
```

### Permission Denied

```bash
# Make scripts executable
chmod +x scripts/*.py

# Or run with python explicitly
python scripts/run_customer_segmentation.py
```

## 📖 Configuration

Edit `config/config.yaml` for:

- Database settings
- Model parameters
- Analytics thresholds
- Agent configurations
- Logging levels

## 🚨 Common Issues

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError | Ensure venv is activated, run `pip install -r requirements.txt` |
| Database connection failed | Check DB_URL in .env, ensure database exists |
| Out of memory | Reduce batch sizes in config.yaml or use PostgreSQL |
| Model download timeout | Download models separately, check internet connection |
| Permission denied | Run with `python` explicitly or `chmod +x` scripts |

## 📚 Additional Resources

- **README.md** - Full platform documentation
- **CONTRIBUTING.md** - How to contribute
- **CHANGELOG.md** - Version history
- **LICENSE** - MIT License

## ✅ What's Next?

1. **Explore the Data**: Check `data/processed/` for analysis results
2. **Review Models**: Check `models/` for trained models
3. **Customize**: Edit `config/config.yaml` for your needs
4. **Extend**: Add your own analytics or agents
5. **Deploy**: Follow cloud deployment guides

## 🤝 Getting Help

- Check README.md for detailed documentation
- Open an issue on GitHub
- Join discussions in GitHub Discussions
- See CONTRIBUTING.md for contribution guidelines

---

**Happy analyzing! 🎉**
