# Contributing to Banking AI Analytics Platform

We welcome contributions to this open-source project! Here's how you can help:

## Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Open a Pull Request

## Code Standards

- Follow PEP 8 for Python code
- Use type hints where possible
- Write docstrings for all functions
- Add unit tests for new features
- Run `black` for code formatting: `black src/`
- Run `flake8` for linting: `flake8 src/`

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Documentation

- Update README.md for feature documentation
- Add docstrings following Google style guide
- Include examples in docstrings
- Update this CONTRIBUTING.md if needed

## Areas for Contribution

- Advanced ML models (XGBoost, LightGBM, neural networks)
- Real-time streaming analytics (Apache Kafka integration)
- Cloud deployment (Azure, AWS, GCP)
- Dashboard development (Grafana, Power BI)
- API endpoints (FastAPI, Flask)
- Multi-language support
- Performance optimization

## Questions?

Open an issue or start a discussion in the GitHub repo.

Thank you for contributing! 🚀
