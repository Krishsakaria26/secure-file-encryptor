# Contributing to Secure File Encryptor

Thank you for your interest in contributing! Here are guidelines to help you get started.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/secure-file-encryptor.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`

## Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes and test thoroughly
3. Commit with clear messages: `git commit -m "Add feature description"`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Create a Pull Request with a detailed description

## Testing

Run tests before submitting PRs:
```bash
python -m src.encrypt --file test_file.txt
python -m src.decrypt --file test_file.txt.enc --out recovered.txt
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable/function names
- Add docstrings to functions
- Keep functions focused and modular

## Bug Reports

Include:
- Python version
- OS and environment
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

## Feature Requests

Describe:
- Use case and motivation
- Expected behavior
- Possible implementation approach

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Open an issue or start a discussion on GitHub!
