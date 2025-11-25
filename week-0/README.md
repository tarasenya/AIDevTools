# Django TODO Application

A simple TODO application built with Django 5.2.8 that allows users to create, manage, and track tasks.

## Features

- Create, edit, and delete TODO items
- Assign due dates to tasks
- Mark TODOs as resolved/completed
- Admin panel for easy management
- Search and filter functionality

## Tech Stack

- Python 3.13
- Django 5.2.8
- SQLite database
- uv for package management

## Project Structure

```
week-0/
├── manage.py              # Django management script
├── Makefile              # Common development commands
├── todoproject/          # Project configuration
│   ├── settings.py       # Project settings
│   ├── urls.py          # URL configuration
│   └── wsgi.py          # WSGI application
└── todos/               # TODO app
    ├── models.py        # Todo model definition
    ├── admin.py         # Admin panel configuration
    ├── views.py         # View logic
    └── migrations/      # Database migrations
```

## Setup Instructions

### 1. Install Dependencies

```bash
make install
# or
uv add django
```

### 2. Run Migrations

```bash
make makemigrations
make migrate
# or
uv run python manage.py makemigrations
uv run python manage.py migrate
```

### 3. Create Superuser

```bash
make createsuperuser
# or
DJANGO_SUPERUSER_PASSWORD=admin123 uv run python manage.py createsuperuser --noinput --username admin --email admin@example.com
```

**Default credentials:**
- Username: `admin`
- Password: `admin123`

### 4. Start Development Server

```bash
make runserver
# or
uv run python manage.py runserver
```

Access the application at: http://127.0.0.1:8000/
Access the admin panel at: http://127.0.0.1:8000/admin/

## Available Make Commands

- `make help` - Display all available commands
- `make install` - Install project dependencies
- `make migrate` - Apply database migrations
- `make makemigrations` - Create new migrations
- `make runserver` - Start development server
- `make createsuperuser` - Create superuser account
- `make shell` - Open Django shell
- `make test` - Run tests
- `make clean` - Remove cache and database files

## Todo Model

The Todo model includes the following fields:

- `title` (CharField) - Task title (max 200 characters)
- `description` (TextField) - Optional detailed description
- `due_date` (DateField) - Optional due date
- `resolved` (BooleanField) - Completion status (default: False)
- `created_at` (DateTimeField) - Auto-generated creation timestamp
- `updated_at` (DateTimeField) - Auto-updated modification timestamp

## Admin Panel Features

- List view with title, due date, resolved status, and creation date
- Quick edit resolved status directly from list view
- Filter by resolved status, due date, and creation date
- Search by title or description
- Date hierarchy navigation for due dates

## Testing

The project includes comprehensive test coverage for all functionality.

### Running Tests

```bash
# Run all tests
make test
# or
uv run python manage.py test

# Run tests for specific app
uv run python manage.py test todos

# Run tests with verbose output
uv run python manage.py test --verbosity=2

# Run specific test class
uv run python manage.py test todos.tests.TodoModelTest

# Run specific test method
uv run python manage.py test todos.tests.TodoModelTest.test_create_todo_with_all_fields
```

### Test Coverage

The test suite covers:

**Model Tests** (`TodoModelTest`):
- Creating todos with all fields
- Creating todos with minimal required fields
- String representation
- Default values
- Ordering by creation date

**View Tests** (`TodoViewTest`):
- List view displays all todos
- Empty list view message
- Create view (GET and POST)
- Update view (GET and POST)
- Delete view (GET and POST)
- Toggle resolved functionality

**Form Tests** (`TodoFormTest`):
- Valid form data
- Minimal data validation
- Missing required fields
- Empty field validation

**URL Tests** (`TodoURLTest`):
- All URL patterns resolve correctly
