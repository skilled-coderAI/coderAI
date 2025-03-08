# Contributing to CoderAI

This guide is intended to help you get started contributing to CoderAI. As an open-source AI integration platform, we welcome contributions in the form of new features, improved infrastructure, better documentation, or bug fixes.

To contribute to this project, please follow the [fork and pull request](https://docs.github.com/en/get-started/quickstart/contributing-to-projects) workflow.

## Reporting Bugs or Suggesting Improvements

Our [GitHub Issues](https://github.com/yourusername/coderAI/issues) page is where we track bugs, improvements, and feature requests. When creating an issue, please:

- **Describe your issue thoroughly:** Provide as many details as possible about what's going wrong. _How_ is it failing? Is there an error message? "It doesn't work" isn't helpful for tracking down problems.

- **Include relevant code:** Share the code that's causing the issue, but only include the relevant parts. This makes it easier for us to reproduce and fix the problem.

- **Format long code blocks:** When sharing long blocks of code or logs, wrap them in `<details>` and `</details>` tags. This collapses the content making the issue easier to read.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/coderAI.git
   cd coderAI
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```

## Code Style Guidelines

- Follow PEP 8 style guidelines for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Write clear commit messages following conventional commits format
- Include docstrings for functions and classes
- Write tests for new features

## Opening a Pull Request

Before submitting a pull request:

1. Test your changes thoroughly
2. Update documentation if needed
3. Ensure all tests pass
4. Rebase your branch on the latest main branch

When creating the pull request:

- Use a clear title following semantic commit conventions
  - Example: `feat: add new AI model integration`
  - Example: `fix: resolve issue with GitHub authentication`
- Provide a detailed description of your changes
- Link any related issues
- Ensure CI checks pass

## Questions and Discussions

If you need help or want to discuss ideas:

- Open a [Discussion](https://github.com/yourusername/coderAI/discussions) for general questions
- Join our community channels (if available)
- Check existing issues and discussions before creating new ones

We aim to review all contributions promptly and provide constructive feedback. Thank you for helping improve CoderAI!