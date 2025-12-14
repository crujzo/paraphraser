# Contributing to AI Paraphraser

First off, thank you for considering contributing to AI Paraphraser! It's people like you that make this tool better for everyone.

## 🎯 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

**Bug Report Template:**

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g. macOS, Windows, Linux]
 - Python Version: [e.g. 3.9]
 - Browser (if web UI): [e.g. Chrome, Safari]

**Additional context**
Any other context about the problem.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any alternative solutions you've considered**

### Pull Requests

1. **Fork the repo** and create your branch from `main`
2. **Make your changes** with clear, descriptive commit messages
3. **Add tests** if you're adding functionality
4. **Update documentation** as needed
5. **Ensure tests pass**
6. **Submit a pull request**

## 🚀 Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/ai-paraphraser.git
cd ai-paraphraser

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python quick_test.py
```

## 📝 Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use descriptive variable names
- Add docstrings to functions and classes

### Example:

```python
def paraphrase(text: str, num_paraphrases: int = 5) -> List[str]:
    """
    Generate multiple paraphrases of the input text.
    
    Args:
        text: Input text to paraphrase
        num_paraphrases: Number of paraphrases to generate
    
    Returns:
        List of paraphrased texts
    """
    # Implementation here
    pass
```

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Start with a capital letter
- Keep first line under 50 characters
- Add detailed description if needed

**Good commit messages:**
```
Add batch processing feature

- Implement batch_paraphrase method
- Add tests for batch processing
- Update documentation
```

**Bad commit messages:**
```
fixed stuff
update
changes
```

## 🧪 Testing

- Add tests for new features
- Ensure all existing tests pass
- Test on multiple platforms if possible

```bash
# Run all tests
python quick_test.py

# Test specific functionality
python -c "from paraphraser import AIParaphraser; p = AIParaphraser(); print(p.paraphrase('test', 3))"
```

## 📚 Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update code comments as needed
- Add examples for new features

## 🎨 Areas for Contribution

### High Priority
- [ ] Multi-language support
- [ ] Improved error handling
- [ ] Performance optimizations
- [ ] Additional model support

### Medium Priority
- [ ] Better test coverage
- [ ] UI/UX improvements
- [ ] Documentation improvements
- [ ] Example notebooks

### Good First Issues
- [ ] Fix typos in documentation
- [ ] Add more usage examples
- [ ] Improve error messages
- [ ] Add input validation

## 🤝 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of:
- Age
- Body size
- Disability
- Ethnicity
- Gender identity and expression
- Level of experience
- Nationality
- Personal appearance
- Race
- Religion
- Sexual identity and orientation

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards others

**Unacceptable behavior includes:**
- Harassment of any kind
- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

## 📋 Pull Request Process

1. **Update documentation** with details of changes
2. **Update the README.md** if adding new features
3. **Add tests** for new functionality
4. **Ensure CI passes** (if configured)
5. **Request review** from maintainers
6. **Be patient and responsive** to feedback

### PR Checklist

- [ ] Code follows the style guidelines
- [ ] Self-review completed
- [ ] Code is commented where needed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] Tests pass locally
- [ ] No breaking changes (or documented if necessary)

## 🎓 Learning Resources

### New to Open Source?
- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [First Contributions](https://github.com/firstcontributions/first-contributions)

### Git & GitHub
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [Understanding the GitHub Flow](https://guides.github.com/introduction/flow/)

### Python
- [Python Documentation](https://docs.python.org/3/)
- [Real Python Tutorials](https://realpython.com/)

## 💬 Getting Help

- 📖 Check the [README](README.md) first
- 🔍 Search existing [issues](https://github.com/yourusername/ai-paraphraser/issues)
- 💬 Start a [discussion](https://github.com/yourusername/ai-paraphraser/discussions)
- 📧 Contact maintainers if needed

## 🌟 Recognition

All contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to AI Paraphraser! 🎉
