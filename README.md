# Banking AI Analytics Platform - UAE

🏦 **Production-Ready AI Platform for UAE Banking Analytics & Compliance**

A comprehensive, open-source artificial intelligence platform built for UAE banks to perform advanced analytics, generative AI tasks, and autonomous agent-based operations. Built with Python, HuggingFace models, and LangChain—no proprietary APIs required.

---

## 🎯 Overview

This platform delivers:

- **📊 Advanced Analytics**: Customer segmentation, credit risk scoring, fraud detection, branch performance analysis, digital channel insights, and product profitability
- **🤖 Generative AI**: KYC summaries, complaint summaries, and credit policy Q&A with RAG
- **🦾 Autonomous Agents**: Customer support, fraud investigation, and compliance monitoring
- **💾 Production Database**: 11-table schema with 8 sample customers and realistic data
- **📈 Fully Configurable**: YAML-based settings, environment variables, and extensible architecture

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    BANKING AI PLATFORM                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐  ┌─────────────────┐  ┌────────────┐ │
│  │  DATA LAYER      │  │  ANALYTICS      │  │  GEN AI    │ │
│  ├──────────────────┤  ├─────────────────┤  ├────────────┤ │
│  │ • PostgreSQL     │  │ • Segmentation  │  │ • KYC      │ │
│  │ • SQLAlchemy ORM │  │ • Credit Risk   │  │ • Complaint│ │
│  │ • 11 Core Tables │  │ • Fraud Detect  │  │ • RAG-QA   │ │
│  │ • Seed Data      │  │ • Performance   │  │            │ │
│  │ • Config YAML    │  │ • Digital       │  │            │ │
│  │                  │  │ • Profitability │  │            │ │
│  └──────────────────┘  └─────────────────┘  └────────────┘ │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            AUTONOMOUS AGENTS (LangChain)             │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │ • Customer Support Agent    • Fraud Investigation    │  │
│  │ • Compliance Agent                                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 What's Included

### Database (11 Tables)
1. **BRANCHES** - Bank location data
2. **CUSTOMERS** - Customer master with UAE/GCC-specific fields
3. **PRODUCTS** - Banking products
4. **ACCOUNTS** - Customer accounts
5. **TRANSACTIONS** - High-volume transaction records
6. **LOANS** - Loan portfolio with NPL tracking
7. **CARDS** - Card portfolio
8. **DIGITAL_CHANNEL_EVENTS** - Digital interaction tracking
9. **KYC_DOCUMENTS** - KYC verification documents
10. **COMPLAINTS** - Customer complaint tracking
11. **RISK_FACTORS** - Risk assessment data

### Analytics Modules (6 Workflows)
- 🎯 **Customer Segmentation**: RFM analysis + K-Means clustering → 4 segments
- 📈 **Credit Risk Scoring**: Logistic regression → NPL prediction probability
- 🚨 **Fraud Detection**: Isolation Forest → Suspicious transaction flags
- 🏢 **Branch Performance**: KPI analysis → Revenue, transaction, complaint metrics
- 📱 **Digital Channel Analytics**: Usage patterns → Device preferences, engagement scores
- 💰 **Product Profitability**: Revenue analysis → Profitability per product

### Generative AI (3 Components)
- 📄 **KYC Summary Generator**: Flan-T5 → Professional KYC summaries
- 💬 **Complaint Summary Generator**: BART → Summaries + resolution suggestions
- 🎓 **Credit Advisory Assistant**: RAG with FAISS → Policy Q&A

### Autonomous Agents (3 Agents)
- 💼 **Customer Support Agent**: Account balance, transactions, complaints
- 🔍 **Fraud Investigation Agent**: Suspicious transactions, risk profiles, pattern analysis
- ⚖️ **Compliance Agent**: KYC status, AML risk, document expiry tracking

### Sample Data
- ✅ 8 realistic customers (UAE nationals, GCC nationals, expats)
- ✅ 10 accounts with realistic balances
- ✅ 8 loans with NPL scenarios
- ✅ 7 credit cards
- ✅ 20+ transactions across channels
- ✅ Digital channel events and complaints
- ✅ Complete KYC documents and risk assessments

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/saisachindas/banking-ai-analytics-uae.git
cd banking-ai-analytics-uae
```

### 2. Install Dependencies
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Setup Database
```bash
# Option A: PostgreSQL (Production)
# Set environment variable
export DB_URL=postgresql://user:password@localhost:5432/uae_banking

# Option B: SQLite (Development - Default)
# Uses SQLite by default: sqlite:///./uae_banking.db

# Create tables and load seed data
sqlite3 uae_banking.db < db/create_tables.sql
sqlite3 uae_banking.db < db/seed_data.sql

# Or with PostgreSQL
psql -U user -d uae_banking -f db/create_tables.sql
psql -U user -d uae_banking -f db/seed_data.sql
```

### 4. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings (optional, defaults work)
vim .env
```

### 5. Run Your First Analysis
```bash
# Customer Segmentation
python scripts/run_customer_segmentation.py

# Credit Risk Scoring
python scripts/run_credit_risk_scoring.py

# Fraud Detection
python scripts/run_fraud_detection.py

# All other analyses
python scripts/run_*.py
```

---

## 📊 Running Analytics

### Customer Segmentation
```bash
python scripts/run_customer_segmentation.py
```
**Output**: `data/processed/customer_segments.csv`
- RFM scores for each customer
- Cluster assignments (4 segments)
- Segment characteristics

### Credit Risk Scoring
```bash
python scripts/run_credit_risk_scoring.py
```
**Output**: 
- `models/credit_risk_model.pkl` (trained model)
- `models/credit_risk_scaler.pkl` (feature scaler)
- Metrics: Training accuracy, test accuracy, ROC-AUC

### Fraud Detection
```bash
python scripts/run_fraud_detection.py
```
**Output**: `data/processed/fraud_alerts.csv`
- Flagged suspicious transactions
- Anomaly scores
- Fraud indicators (night transactions, weekend, large amounts)

### Branch Performance
```bash
python scripts/run_branch_performance.py
```
**Output**: `data/processed/branch_performance.csv`
- Revenue per employee
- Transaction volume
- Customer satisfaction (complaint resolution)
- Loan-to-deposit ratio

### Digital Channel Analytics
```bash
python scripts/run_digital_channel_analytics.py
```
**Output**: `data/processed/digital_channel_kpis.csv`
- Channel usage patterns
- Device preferences
- Engagement scores
- Session metrics

### Product Profitability
```bash
python scripts/run_product_profitability.py
```
**Output**: `data/processed/product_profitability_report.csv`
- Annual revenue by product
- Revenue per account
- Interest and fee income
- Profitability rankings

---

## 🤖 Using Generative AI

### KYC Summary
```python
from src.genai.kyc_summary_generator import generate_kyc_summary

# Generate professional KYC summary
summary = generate_kyc_summary(customer_id=1)
print(summary['kyc_summary'])
print(summary['recommendations'])
```

### Complaint Summaries
```python
from src.genai.complaint_summary_generator import generate_complaint_summaries

# Generate summaries for open complaints
python scripts/run_complaint_summary_generator.py
```

### Credit Policy Q&A (RAG)
```python
from src.genai.credit_advisory_assistant import CreditPolicyAdvisor

advisor = CreditPolicyAdvisor()
answer = advisor.answer_question("What are the credit limits for UAE nationals?")
print(answer)
```

---

## 🦾 Using Autonomous Agents

### Customer Support Agent
```bash
python scripts/run_customer_support_agent.py
```

**Capabilities**:
- Get account balance
- Retrieve recent transactions
- Raise complaints
- Check card status

### Fraud Investigation Agent
```bash
python scripts/run_fraud_investigation_agent.py
```

**Capabilities**:
- Find flagged transactions
- Get customer risk profiles
- Analyze transaction patterns
- Flag accounts for review

### Compliance Agent
```bash
python scripts/run_compliance_agent.py
```

**Capabilities**:
- Check KYC status
- Get AML risk assessment
- List expiring documents
- Generate compliance dashboard

---

## 🔧 Development

### Project Structure
```
banking-ai-analytics-uae/
├── src/
│   ├── db/                      # Database layer
│   │   ├── connection.py        # SQLAlchemy setup
│   │   └── __init__.py
│   ├── analytics/               # Analytics module
│   │   ├── customer_segmentation.py
│   │   ├── credit_risk_scoring.py
│   │   ├── fraud_detection.py
│   │   ├── branch_performance.py
│   │   ├── digital_channel_analytics.py
│   │   ├── product_profitability.py
│   │   └── __init__.py
│   ├── genai/                   # Generative AI module
│   │   ├── kyc_summary_generator.py
│   │   ├── complaint_summary_generator.py
│   │   ├── credit_advisory_assistant.py
│   │   └── __init__.py
│   ├── agents/                  # Agentic AI module
│   │   ├── customer_support_agent.py
│   │   ├── fraud_investigation_agent.py
│   │   ├── compliance_agent.py
│   │   └── __init__.py
│   └── __init__.py
├── db/
│   ├── create_tables.sql        # DDL for 11 tables
│   └── seed_data.sql            # Sample data
├── scripts/                     # Executable run scripts
│   ├── run_customer_segmentation.py
│   ├── run_credit_risk_scoring.py
│   ├── run_fraud_detection.py
│   ├── run_branch_performance.py
│   ├── run_digital_channel_analytics.py
│   ├── run_product_profitability.py
│   ├── run_complaint_summary_generator.py
│   ├── run_customer_support_agent.py
│   ├── run_fraud_investigation_agent.py
│   └── run_compliance_agent.py
├── config/
│   └── config.yaml              # Configuration file
├── data/
│   ├── raw/                     # Raw data
│   │   └── policy_docs/         # Sample policy documents
│   └── processed/               # Processed results
├── models/                      # Trained models
├── logs/                        # Log files
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── README.md                    # This file
├── CONTRIBUTING.md              # Contributing guidelines
├── CHANGELOG.md                 # Version history
├── LICENSE                      # MIT License
└── .gitignore                   # Git ignore rules
```

### Code Standards
- **Style**: PEP 8 (use `black` for formatting)
- **Linting**: `flake8`
- **Type Hints**: Use throughout
- **Docstrings**: Google style
- **Testing**: `pytest` for unit tests

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📋 System Requirements

- **Python**: 3.9 or higher
- **Database**: PostgreSQL 12+ (production) or SQLite 3.0+ (development)
- **RAM**: 8GB minimum (16GB recommended for ML models)
- **Storage**: 10GB for models and data
- **GPU**: Optional (for faster inference on large datasets)

---

## 🔑 Configuration

All settings are in `config/config.yaml`. Key options:

```yaml
# Database
database:
  url: "postgresql://user:pass@localhost/uae_banking"
  pool_size: 10

# Models
models:
  text_generation: "google/flan-t5-large"
  embedding: "sentence-transformers/all-MiniLM-L6-v2"
  device: "cpu"  # or "cuda"

# Analytics
analytics:
  fraud_contamination: 0.05
  segmentation_clusters: 4
  credit_risk_npl_threshold: 0.5
```

---

## 📚 Documentation

Full documentation for each module:

- **Database**: Docstrings in `src/db/connection.py`
- **Analytics**: Docstrings in `src/analytics/*.py`
- **GenAI**: Docstrings in `src/genai/*.py`
- **Agents**: Docstrings in `src/agents/*.py`

All functions include usage examples in their docstrings.

---

## 🎯 Use Cases

### Risk Management
- Identify high-risk customers with AML scoring
- Monitor PEP (Politically Exposed Persons) customers
- Track KYC document expiration
- Predict NPL (Non-Performing Loans)

### Revenue Optimization
- Segment customers for targeted marketing
- Analyze product profitability
- Optimize branch operations
- Improve digital channel engagement

### Compliance
- Monitor regulatory requirements
- Generate compliance reports
- Track document verification
- Manage complaint resolution

### Operations
- Detect fraudulent transactions in real-time
- Automate customer support
- Analyze branch performance
- Optimize product offerings

---

## 🔄 Workflow Examples

### Complete Risk Assessment
```python
from src.analytics.credit_risk_scoring import build_credit_risk_model
from src.analytics.fraud_detection import detect_fraud_anomalies
from src.agents.compliance_agent import ComplianceAgent

# 1. Train credit risk model
model, scaler, metrics = build_credit_risk_model()

# 2. Detect fraud
alerts = detect_fraud_anomalies()

# 3. Compliance review
agent = ComplianceAgent()
report = agent.generate_report()
```

### Customer Insights Pipeline
```python
from src.analytics.customer_segmentation import compute_rfm_segments
from src.analytics.digital_channel_analytics import analyze_digital_channels
from src.genai.kyc_summary_generator import generate_kyc_summary

# 1. Segment customers
segments = compute_rfm_segments()

# 2. Analyze digital behavior
channel_data = analyze_digital_channels()

# 3. Generate KYC summaries
for customer_id in range(1, 9):
    summary = generate_kyc_summary(customer_id)
```

---

## 📊 Sample Data

### Customers
- **Ahmed Al Mansouri** (Premium, PEP flag)
- **Fatima Al Noor** (Standard)
- **Mohammed Al Suwaidi** (Premium, PEP)
- **Layla Al Khaleej** (GCC National)
- **Abdullah Al Mazrouei** (Corporate)
- **Noor Al Shamsi** (Mass Market)
- **Khaled Al Mansoori** (Premium)
- **Zainab Al Kaabi** (Dormant)

### Transactions
- Salary deposits
- Bill payments (DEWA)
- Shopping (Carrefour, Lulu)
- Business transfers
- Loan payments
- Cash withdrawals (some fraudulent)

### Loans
- Personal loans
- Home loans (mortgages)
- Auto loans
- Business loans
- Some with NPL flags

---

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Test connection
python -c "from src.db.connection import test_connection; test_connection()"
```

### Missing Dependencies
```bash
# Reinstall requirements
pip install --force-reinstall -r requirements.txt
```

### Model Download Errors
```bash
# Pre-download HuggingFace models
python -c "from transformers import AutoModel; AutoModel.from_pretrained('google/flan-t5-base')"
```

---

## 📈 Performance Tips

1. **Use PostgreSQL** for production (SQLite is for development only)
2. **Enable GPU** if available for model inference
3. **Batch processing** for large datasets
4. **Index frequently queried columns** in database
5. **Cache embeddings** for RAG system
6. **Use connection pooling** for database

---

## 🔐 Security Notes

- **Never commit `.env`** with real credentials
- **Use strong database passwords** in production
- **Enable SSL** for PostgreSQL connections
- **Mask PII** in logs and outputs
- **Validate all inputs** to database queries
- **Use parameterized queries** (SQLAlchemy does this by default)

---

## 📞 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

Copyright (c) 2024 Banking AI Analytics Contributors

---

## 🚀 Roadmap

### v1.1.0 (Q3 2024)
- Real-time streaming analytics (Kafka)
- Advanced models (XGBoost, LightGBM)
- REST API (FastAPI)
- Web dashboard (Streamlit)

### v1.2.0 (Q4 2024)
- Cloud deployment (Azure, AWS)
- Multi-tenant support
- CI/CD pipelines
- Performance optimization

### v2.0.0 (H1 2025)
- Deep learning models
- Multi-language support
- Enhanced RAG capabilities
- Advanced reporting

---

## ⭐ Star Us!

If you find this useful, please ⭐ the repository!

---

**Built with ❤️ for UAE Banks | Open Source | Production Ready**
