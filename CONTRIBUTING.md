# Contributing to RoyaleForge

Thank you for your interest in contributing to RoyaleForge. This document provides guidelines and instructions for contributing.

## Table of Contents

- Development Setup
- Project Architecture
- Coding Standards
- Commit Guidelines
- Pull Request Process
- Testing

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- Modern web browser (Chrome, Firefox, Edge)

### Installation

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/ShauryaSingh1709/Clash-Royale.git
cd Clash-Royale
```

3. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Generate the dataset:

```bash
python scripts/generate_dataset.py
```

6. Start the development server:

```bash
python -m backend.app
```

## Project Architecture

### Backend Structure

```
backend/
├── app.py                      # Flask application factory
├── config/
│   └── settings.py             # Configuration and environment variables
├── models/                     # Data models (Card, Deck, Battle)
├── routes/                     # API route handlers
├── services/                   # Business logic layer
├── ml/                         # Machine learning models
└── utils/                      # Helper utilities
```

### Frontend Structure

```
frontend/
├── css/                        # Stylesheets
├── js/                         # JavaScript modules
│   ├── analyzer.js             # Deck analyzer page logic
│   ├── cards.js                # Card explorer logic
│   ├── dashboard.js            # Dashboard charts
│   └── navbar.js               # Navigation and footer
└── *.html                      # Page templates
```

### Data Pipeline

1. **scripts/generate_dataset.py** - Generates synthetic card, deck, and battle data
2. **notebooks/02_data_cleaning.ipynb** - Cleans and processes raw data
3. **notebooks/04_ml_model_training.ipynb** - Trains ML models
4. **backend/ml/model_loader.py** - Loads trained models into memory

## Coding Standards

### Python

- Follow PEP 8 style guide
- Use type hints for function signatures
- Use snake_case for variables and functions
- Use PascalCase for classes
- Keep functions focused and single-purpose
- Use meaningful variable names

### JavaScript

- Use ES6+ syntax (const, let, arrow functions)
- Prefer async/await over promise chains
- Use camelCase for variables and functions
- Keep functions small and pure when possible

### CSS

- Use CSS variables from the design system
- Follow BEM-like naming for new components
- Mobile-first responsive design
- Avoid !important unless absolutely necessary

## Commit Guidelines

Use Conventional Commits format:

```
<type>(<scope>): <description>
```

Types:

- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Formatting changes
- `refactor` - Code refactoring
- `test` - Adding or updating tests
- `chore` - Maintenance tasks

Examples:

```
feat(analyzer): add deck export functionality
fix(api): correct rarity filter parameter
docs(readme): update installation instructions
style(navbar): improve mobile responsiveness
refactor(ml): optimize model loading
test(decks): add validation tests
```

## Pull Request Process

1. Create a feature branch from main:

```bash
git checkout -m feature/descriptive-name
```

2. Make your changes with clear, focused commits

3. Ensure code follows the coding standards

4. Test your changes locally:

```bash
python -m backend.app
```

5. Push to your fork:

```bash
git push origin feature/descriptive-name
```

6. Open a Pull Request on GitHub with:

   - Clear description of changes
   - Reference to any related issues
   - Screenshots for UI changes (if applicable)

### PR Requirements

- Code must run without errors
- All existing functionality must remain intact
- Tests should pass (if test infrastructure exists)
- Documentation should be updated for new features

## Testing

Run tests with:

```bash
python -m pytest backend/tests/
```

Or run individual test files:

```bash
python -m pytest backend/tests/test_models.py
python -m pytest backend/tests/test_services.py
python -m pytest backend/tests/test_ml.py
```

## Questions or Issues

- Open an issue on GitHub for bugs or feature requests
- Check existing issues before creating new ones
- Provide detailed reproduction steps for bugs

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers and help them get started
- Accept feedback gracefully
- Focus on what is best for the community

---

By contributing, you agree that your contributions will be licensed under the MIT License.