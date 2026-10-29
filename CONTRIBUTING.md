# 🤝 Contributing to CodeGuard AI

Thank you for your interest in contributing to **CodeGuard AI**! Contributions, bug fixes, suggestions, documentation updates, and feature improvements are welcome.

This guide explains how to contribute while keeping the project organized, reliable, and easy to maintain.

---

## How to Contribute

### 1. Fork the Repository

Open the CodeGuard AI repository on GitHub and click **Fork** to create your own copy.

### 2. Clone Your Fork

Replace `your-username` with your GitHub username.

```bash
git clone https://github.com/your-username/CodeGuardAI.git
cd CodeGuardAI
```

### 3. Create a Branch

Create a separate branch for your changes.

```bash
git checkout -b feature/your-feature-name
```

For bug fixes, you can use:

```bash
git checkout -b fix/your-bug-name
```

### 4. Set Up the Development Environment

Create and activate a virtual environment.

```bash
py -3.13 -m venv .venv
```

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

### 5. Make Your Changes

You may contribute by:

- Fixing bugs in code analysis
- Improving security checks
- Enhancing the Streamlit interface
- Improving AI-generated review instructions
- Adding useful finding filters
- Improving CSV export functionality
- Writing or updating tests
- Improving documentation
- Optimizing performance
- Suggesting additional analysis tools

Keep your changes focused and consistent with the existing project structure.

### 6. Test Your Changes

Run the existing tests before submitting your work.

```bash
python -m pytest
```

You can also run the local analysis tools directly:

```bash
python -m ruff check .
python -m bandit -r .
```

Review the results carefully. If a command reports issues in your own contribution, address them where appropriate. Avoid unrelated changes to existing code.

If you modify AI functionality, test it with a valid API key stored in your local `.env` file. Never include that key in your commits, test fixtures, screenshots, or pull requests.

### 7. Commit Your Changes

Use a clear commit message that describes what you changed.

```bash
git add .
git commit -m "Improve code analysis results"
```

Other examples:

```bash
git commit -m "Fix CSV export handling"
git commit -m "Improve AI review instructions"
git commit -m "Add analyzer tests"
```

### 8. Push Your Branch

```bash
git push origin feature/your-feature-name
```

### 9. Submit a Pull Request

Open your fork on GitHub and create a Pull Request against the original repository.

Include:

- A clear summary of your changes
- The reason for the change
- Relevant test results
- Screenshots for interface changes, if applicable
- Any limitations or known issues

---

## Development Guidelines

To keep CodeGuard AI maintainable and reliable, please follow these practices:

- Write clean, readable Python code.
- Use meaningful variable, function, and file names.
- Keep functions focused on a clear responsibility.
- Follow the existing project structure.
- Avoid unnecessary dependencies.
- Handle errors gracefully and provide useful messages.
- Add tests for new functionality when practical.
- Update the documentation when behavior or setup instructions change.
- Avoid logging API keys, passwords, tokens, or confidential code.
- Keep changes focused instead of modifying unrelated parts of the project.

---

## Security Guidelines

Because CodeGuard AI handles source code and security-related findings, contributors should take extra care when making changes.

- Never commit `.env` files or real API credentials.
- Do not use real secrets in examples, tests, or screenshots.
- Treat submitted source code as potentially sensitive.
- Do not execute scanned code automatically unless a feature explicitly requires it and appropriate safeguards are implemented.
- Validate user input and handle malformed source code safely.
- Review AI-generated suggestions rather than treating them as verified security fixes.
- Report potentially serious security vulnerabilities privately to the project maintainer instead of publishing exploit details in a public issue.

---

## Reporting Bugs

If you discover a bug, open a GitHub Issue and include:

- A clear description of the problem
- Steps to reproduce it
- Expected behavior
- Actual behavior
- Relevant error messages or logs
- Python version and operating system
- The affected feature or module

Remove API keys, passwords, private source code, and other sensitive information before sharing logs or screenshots.

---

## Suggesting Features

Feature suggestions are welcome.

When proposing an improvement, explain:

- What the feature should do
- What problem it solves
- How it would benefit users
- Any implementation ideas or examples

Possible areas for future development include:

- Additional programming-language support
- More security and linting integrations
- Improved AI review explanations
- PDF report generation
- Scan history
- GitHub integration
- Custom analysis rules
- Improved reporting and filtering

These are suggestions for future development, not a guarantee that they are already implemented.

---

## Code Style and Tools

CodeGuard AI uses Python and Streamlit, with Bandit and Ruff supporting selected security and code-quality checks.

Contributors should:

- Maintain compatibility with the project's supported Python version.
- Follow the formatting and linting conventions used by the project.
- Keep static analysis separate from AI review logic where practical.
- Use environment variables for API configuration.
- Write tests that are repeatable and do not depend on private credentials.
- Keep dependencies documented in `requirements.txt`.

---

## Pull Request Checklist

Before submitting a Pull Request, confirm the following:

- [ ] The application starts successfully.
- [ ] The changes work as intended.
- [ ] Existing functionality has not been unintentionally broken.
- [ ] Tests have been run where applicable.
- [ ] Static-analysis findings have been reviewed.
- [ ] Documentation has been updated if necessary.
- [ ] No API keys or confidential information are included.
- [ ] Commit messages clearly describe the changes.

---

## License

Contributions will be subject to the license selected for CodeGuard AI. Please check the repository's `LICENSE` file before submitting contributions.

Thank you for helping improve **CodeGuard AI** and supporting secure, responsible software development!
