from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
from .models import Todo
from .forms import TodoForm


class TodoModelTest(TestCase):
    """Test cases for the Todo model."""

    def test_create_todo_with_all_fields(self):
        """Test creating a Todo with all fields populated."""
        todo = Todo.objects.create(
            title="Test Todo",
            description="Test description",
            due_date=date.today() + timedelta(days=7),
            resolved=False
        )
        self.assertEqual(todo.title, "Test Todo")
        self.assertEqual(todo.description, "Test description")
        self.assertIsNotNone(todo.due_date)
        self.assertFalse(todo.resolved)
        self.assertIsNotNone(todo.created_at)
        self.assertIsNotNone(todo.updated_at)

    def test_create_todo_with_minimal_fields(self):
        """Test creating a Todo with only required fields."""
        todo = Todo.objects.create(title="Minimal Todo")
        self.assertEqual(todo.title, "Minimal Todo")
        self.assertEqual(todo.description, "")
        self.assertIsNone(todo.due_date)
        self.assertFalse(todo.resolved)

    def test_todo_str_representation(self):
        """Test the string representation of Todo."""
        todo = Todo.objects.create(title="Test Todo")
        self.assertEqual(str(todo), "Test Todo")

    def test_todo_default_resolved_is_false(self):
        """Test that resolved defaults to False."""
        todo = Todo.objects.create(title="Test Todo")
        self.assertFalse(todo.resolved)

    def test_todo_ordering(self):
        """Test that todos are ordered by creation date (newest first)."""
        todo1 = Todo.objects.create(title="First Todo")
        todo2 = Todo.objects.create(title="Second Todo")
        todo3 = Todo.objects.create(title="Third Todo")

        todos = Todo.objects.all()
        self.assertEqual(todos[0], todo3)
        self.assertEqual(todos[1], todo2)
        self.assertEqual(todos[2], todo1)


class TodoViewTest(TestCase):
    """Test cases for Todo views."""

    def setUp(self):
        """Set up test data."""
        self.todo1 = Todo.objects.create(
            title="Test Todo 1",
            description="Description 1",
            due_date=date.today() + timedelta(days=1)
        )
        self.todo2 = Todo.objects.create(
            title="Test Todo 2",
            resolved=True
        )

    def test_todo_list_view(self):
        """Test that the list view displays all todos."""
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_list.html')
        self.assertContains(response, "Test Todo 1")
        self.assertContains(response, "Test Todo 2")

    def test_todo_list_view_empty(self):
        """Test list view with no todos."""
        Todo.objects.all().delete()
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No TODOs yet")

    def test_todo_create_view_get(self):
        """Test GET request to create view displays form."""
        response = self.client.get(reverse('todo_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_form.html')

    def test_todo_create_view_post(self):
        """Test POST request to create view creates a new todo."""
        data = {
            'title': 'New Todo',
            'description': 'New description',
            'due_date': date.today() + timedelta(days=5),
            'resolved': False
        }
        response = self.client.post(reverse('todo_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Todo.objects.filter(title='New Todo').exists())

    def test_todo_update_view_get(self):
        """Test GET request to update view displays form with existing data."""
        response = self.client.get(reverse('todo_update', args=[self.todo1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_form.html')
        self.assertContains(response, "Test Todo 1")

    def test_todo_update_view_post(self):
        """Test POST request to update view modifies the todo."""
        data = {
            'title': 'Updated Todo',
            'description': 'Updated description',
            'due_date': date.today(),
            'resolved': True
        }
        response = self.client.post(reverse('todo_update', args=[self.todo1.pk]), data)
        self.assertEqual(response.status_code, 302)
        self.todo1.refresh_from_db()
        self.assertEqual(self.todo1.title, 'Updated Todo')
        self.assertTrue(self.todo1.resolved)

    def test_todo_delete_view_get(self):
        """Test GET request to delete view displays confirmation."""
        response = self.client.get(reverse('todo_delete', args=[self.todo1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_confirm_delete.html')
        self.assertContains(response, "Test Todo 1")

    def test_todo_delete_view_post(self):
        """Test POST request to delete view removes the todo."""
        todo_pk = self.todo1.pk
        response = self.client.post(reverse('todo_delete', args=[todo_pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(pk=todo_pk).exists())

    def test_toggle_resolved(self):
        """Test toggling the resolved status of a todo."""
        self.assertFalse(self.todo1.resolved)
        response = self.client.get(reverse('todo_toggle', args=[self.todo1.pk]))
        self.assertEqual(response.status_code, 302)
        self.todo1.refresh_from_db()
        self.assertTrue(self.todo1.resolved)

        # Toggle again
        response = self.client.get(reverse('todo_toggle', args=[self.todo1.pk]))
        self.todo1.refresh_from_db()
        self.assertFalse(self.todo1.resolved)


class TodoFormTest(TestCase):
    """Test cases for Todo forms."""

    def test_valid_form(self):
        """Test form with valid data."""
        data = {
            'title': 'Test Todo',
            'description': 'Test description',
            'due_date': date.today() + timedelta(days=1),
            'resolved': False
        }
        form = TodoForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_with_minimal_data(self):
        """Test form with only required field (title)."""
        data = {'title': 'Test Todo'}
        form = TodoForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_missing_title(self):
        """Test form without required title field."""
        data = {
            'description': 'Test description',
            'due_date': date.today()
        }
        form = TodoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_form_with_empty_title(self):
        """Test form with empty title."""
        data = {'title': ''}
        form = TodoForm(data=data)
        self.assertFalse(form.is_valid())


class TodoURLTest(TestCase):
    """Test cases for Todo URLs."""

    def test_todo_list_url_resolves(self):
        """Test that the list URL resolves correctly."""
        url = reverse('todo_list')
        self.assertEqual(url, '/')

    def test_todo_create_url_resolves(self):
        """Test that the create URL resolves correctly."""
        url = reverse('todo_create')
        self.assertEqual(url, '/create/')

    def test_todo_update_url_resolves(self):
        """Test that the update URL resolves correctly."""
        url = reverse('todo_update', args=[1])
        self.assertEqual(url, '/update/1/')

    def test_todo_delete_url_resolves(self):
        """Test that the delete URL resolves correctly."""
        url = reverse('todo_delete', args=[1])
        self.assertEqual(url, '/delete/1/')

    def test_todo_toggle_url_resolves(self):
        """Test that the toggle URL resolves correctly."""
        url = reverse('todo_toggle', args=[1])
        self.assertEqual(url, '/toggle/1/')
