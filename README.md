# Banking AI Analytics Platform for UAE Banks

## 🏦 Project Overview

A **production-ready, open-source Python platform** for analytics, generative AI, and agentic automation designed for UAE-based banking institutions. This platform provides end-to-end solutions for:

- **Analytics**: Customer segmentation, credit risk scoring, fraud detection, branch performance, digital channel analytics, and product profitability.
- **Generative AI**: KYC summaries, complaint summaries, and intelligent credit advisory powered by open-source LLMs.
- **Agentic AI**: Autonomous agents for customer support, fraud investigation, and compliance monitoring.

All powered by **open-source models** (HuggingFace, LangChain, FAISS) and designed to run **locally and on cloud** (Azure preferred).

---

## 🏗️ Architecture Layers

```
┌────────────────────────────────────────────┐
│        Agentic AI Layer                    │
│  (Customer Support, Fraud Investigation,   │
│   Compliance Monitoring)                   │
├────────────────────────────────────────────┤
│        Generative AI Layer                 │
│  (KYC Summaries, Complaint Summaries,      │
│   Credit Advisory RAG)                     │
├────────────────────────────────────────────┤
│        Analytics Layer                     │
│  (Segmentation, Risk, Fraud, Performance)  │
├────────────────────────────────────────────┤
│        Data & Database Layer               │
│  (PostgreSQL/SQLite, SQLAlchemy ORM)       │
└────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.9+ |
| **Database** | PostgreSQL (production) / SQLite (local dev) |
| **ORM** | SQLAlchemy |
| **Analytics** | Pandas, NumPy, Scikit-learn, Statsmodels |
| **Visualization** | Matplotlib, Seaborn, Plotly |
| **LLM Framework** | HuggingFace Transformers, LangChain |
| **Vector DB** | FAISS, ChromaDB |
| **Agentic AI** | LangChain Agents, LangChain Tools |
| **Dev Tools** | Jupyter, Black, Pytest |

---

## 📁 Project Structure

```
banking-ai-analytics-uae/
├── README.md                              # This file
├── requirements.txt                       # Python dependencies
├── .gitignore                            # Git ignore patterns
├── .env.example                          # Environment template
├── config/
│   └── config.yaml                       # Configuration file
├── data/
│   ├── raw/                              # Raw CSV input data
│   │   ├── customers.csv
│   │   ├── accounts.csv
│   │   ├── transactions.csv
│   │   ├── loans.csv
│   │   ├── cards.csv
│   │   ├── branches.csv
│   │   ├── products.csv
│   │   ├── digital_channel_events.csv
│   │   ├── kyc_documents.csv
│   │   ├── complaints.csv
│   │   └── risk_factors.csv
│   └── processed/                        # Output data & indexes
├── db/
│   ├── create_tables.sql                 # Database schema (DDL)
│   └── seed_data.sql                     # Test/demo data
├── notebooks/
│   └── exploration/
│       ├── 01_data_overview.ipynb
│       ├── 02_customer_segmentation.ipynb
│       ├── 03_credit_risk_scoring.ipynb
│       └── 04_fraud_detection.ipynb
├── src/
│   ├── __init__.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── connection.py                 # SQLAlchemy setup
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── customer_segmentation.py      # RFM + K-Means clustering
│   │   ├── branch_performance.py         # Branch KPIs
│   │   ├── credit_risk_scoring.py        # NPL prediction model
│   │   ├── fraud_detection.py            # Isolation Forest anomaly detection
│   │   ├── digital_channel_analytics.py  # Channel usage analytics
│   │   └── product_profitability.py      # Product profitability metrics
│   ├── genai/
│   │   ├── __init__.py
│   │   ├── kyc_summary_generator.py      # KYC document summarizer
│   │   ├── complaint_summary_generator.py# Complaint resolution summarizer
│   │   └── credit_advisory_assistant.py  # RAG-based credit policy advisor
│   └── agents/
│       ├── __init__.py
│       ├── customer_support_agent.py     # Customer service agent
│       ├── fraud_investigation_agent.py  # Fraud investigation agent
│       └── compliance_agent.py           # Compliance monitoring agent
└── scripts/
    ├── run_customer_segmentation.py
    ├── run_branch_performance.py
    ├── run_credit_risk_scoring.py
    ├── run_fraud_detection.py
    ├── run_customer_support_agent.py
    ├── run_fraud_investigation_agent.py
    └── run_compliance_agent.py
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- PostgreSQL 12+ (or use SQLite for local development)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/saisachindas/banking-ai-analytics-uae.git
cd banking-ai-analytics-uae
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration (DB connection, HuggingFace token, etc.)
```

### 5. Initialize the Database

For **PostgreSQL**:
```bash
psql -U postgres -h localhost -d uae_banking -f db/create_tables.sql
psql -U postgres -h localhost -d uae_banking -f db/seed_data.sql
```

For **SQLite** (local development):
```bash
python -c "from src.db.connection import create_all_tables; create_all_tables()"
```

### 6. Load Sample Data (Optional)

Sample CSV files are provided in `data/raw/`. Load them into the database:

```bash
python -c "from src.db.connection import load_csv_to_db; load_csv_to_db('data/raw')"
```

---

## 📊 Running Analytics Workflows

### Customer Segmentation (RFM + K-Means)

```bash
python scripts/run_customer_segmentation.py
# Output: data/processed/customer_segments.csv
```

### Credit Risk Scoring (Logistic Regression)

```bash
python scripts/run_credit_risk_scoring.py
# Output: Credit risk model + predictions
```

### Fraud Detection (Isolation Forest)

```bash
python scripts/run_fraud_detection.py
# Output: data/processed/fraud_alerts.csv
```

### Branch Performance Analysis

```bash
python scripts/run_branch_performance.py
# Output: data/processed/branch_performance.html (interactive dashboard)
```

### Digital Channel Analytics

```bash
python scripts/run_digital_channel_analytics.py
# Output: data/processed/digital_channel_kpis.csv
```

### Product Profitability

```bash
python scripts/run_product_profitability.py
# Output: data/processed/product_profitability_report.csv
```

---

## 🤖 Running Generative AI Pipelines

### KYC Summary Generator

```bash
python -c "from src.genai.kyc_summary_generator import main; main(customer_id=1)"
```

### Complaint Summary Generator

```bash
python scripts/run_complaint_summary_generator.py
# Output: data/processed/complaint_summaries.csv
```

### Credit Advisory Assistant (RAG)

```bash
python -c "from src.genai.credit_advisory_assistant import main; main()"
# Asks: 'What are the credit limits for UAE nationals?'
```

---

## 🤝 Running Agentic AI Agents

### Customer Support Agent

```bash
python scripts/run_customer_support_agent.py
# Example: Agent retrieves account balance, recent transactions, raises complaints
```

### Fraud Investigation Agent

```bash
python scripts/run_fraud_investigation_agent.py
# Example: Agent investigates flagged transactions and generates compliance report
```

### Compliance Agent

```bash
python scripts/run_compliance_agent.py
# Example: Agent monitors KYC status, AML risk, and document expiry
```

---

## 📖 Documentation

Each module includes detailed docstrings. For example:

```python
from src.analytics.customer_segmentation import compute_rfm_segments

help(compute_rfm_segments)
```

### Key Modules

| Module | Purpose |
|--------|---------|
| `src.db.connection` | Database connectivity, session management |
| `src.analytics.*` | Customer and risk analytics |
| `src.genai.*` | LLM-powered summaries and RAG pipelines |
| `src.agents.*` | Autonomous agents with tools |

---

## ⚙️ Configuration

### `config/config.yaml`

```yaml
# Database
database:
  url: "postgresql://postgres:password@localhost:5432/uae_banking"
  echo: false

# LLM Models (HuggingFace)
models:
  text_generation: "google/flan-t5-large"
  embedding: "sentence-transformers/all-MiniLM-L6-v2"

# Analytics Thresholds
analytics:
  fraud_isolation_forest_contamination: 0.05
  credit_risk_npl_threshold: 0.5
  segmentation_clusters: 4

# Paths
paths:
  data_raw: "data/raw"
  data_processed: "data/processed"
  vector_index: "data/processed/credit_policy_index"
```

---

## 🔒 Security & Privacy

- **No hardcoded credentials**: Use `.env` for sensitive data.
- **Open-source models only**: No proprietary API keys required by default.
- **Data anonymization**: Seed data uses realistic but synthetic information.
- **Audit logging**: All agent actions are logged for compliance.

---

## 🧪 Testing

Run unit tests:

```bash
pytest tests/ -v
```

Test coverage for:
- Database connectivity
- RFM segmentation logic
- Credit risk model training
- Fraud detection pipeline
- Agent tool execution

---

## 📈 Extensibility & Future Work

This platform is designed to grow with your bank:

1. **Core System Integration**: Connect to your bank's core system (Temenos, Finacle, etc.)
2. **Real-time Streaming**: Add Apache Kafka for real-time transaction processing
3. **Advanced Models**: Integrate XGBoost, LightGBM, and deep learning models
4. **Cloud Deployment**: Azure Container Registry, AKS, Logic Apps for orchestration
5. **CI/CD**: GitHub Actions for automated testing and deployment
6. **Dashboards**: Grafana/Power BI for real-time monitoring
7. **Multi-tenant Support**: Isolate data by bank subsidiary or geography

---

## 📞 Support & Contribution

This is an **open-source project** designed for UAE banking innovation. Contributions, issues, and feature requests are welcome!

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**. See LICENSE file for details.

---

## 🌟 Acknowledgments

- **HuggingFace**: Open-source transformer models
- **LangChain**: Framework for building with LLMs
- **Scikit-learn**: Machine learning algorithms
- **FAISS**: Vector similarity search
- **SQLAlchemy**: Python SQL toolkit

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

**Happy banking with AI! 🚀**
