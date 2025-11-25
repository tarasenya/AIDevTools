.PHONY: help install migrate makemigrations runserver createsuperuser shell test clean

help:
	@echo "Available commands:"
	@echo "  make install        - Install project dependencies"
	@echo "  make migrate        - Apply database migrations"
	@echo "  make makemigrations - Create new migrations"
	@echo "  make runserver      - Start development server"
	@echo "  make createsuperuser - Create superuser account"
	@echo "  make shell          - Open Django shell"
	@echo "  make test           - Run tests"
	@echo "  make clean          - Remove cache and database files"

install:
	uv add django

migrate:
	uv run python manage.py migrate

makemigrations:
	uv run python manage.py makemigrations

runserver:
	uv run python manage.py runserver

createsuperuser:
	DJANGO_SUPERUSER_PASSWORD=admin123 uv run python manage.py createsuperuser --noinput --username admin --email admin@example.com

shell:
	uv run python manage.py shell

test:
	uv run python manage.py test

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -f db.sqlite3