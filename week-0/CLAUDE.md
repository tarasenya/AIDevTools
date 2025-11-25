# Project Name

## Tech Stack
- Python 3.13
- Django
- uv for package management

## Development Commands
- Start server: `uv run python manage.py runserver`
- Run tests: `uv run python manage.py test`
- Install packages: `uv add <package-name>`

## Code Standards
- Use type hints
- Follow PEP 8
- Write docstrings for all functions

## Important Notes
- Always use `uv add` for installing packages, NOT pip
- Never use `pip install` directly