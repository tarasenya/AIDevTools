from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Todo
from .forms import TodoForm


class TodoListView(ListView):
    """Display list of all TODO items."""

    model = Todo
    template_name = 'todos/todo_list.html'
    context_object_name = 'todos'


class TodoCreateView(CreateView):
    """Create a new TODO item."""

    model = Todo
    form_class = TodoForm
    template_name = 'todos/todo_form.html'
    success_url = reverse_lazy('todo_list')


class TodoUpdateView(UpdateView):
    """Update an existing TODO item."""

    model = Todo
    form_class = TodoForm
    template_name = 'todos/todo_form.html'
    success_url = reverse_lazy('todo_list')


class TodoDeleteView(DeleteView):
    """Delete a TODO item."""

    model = Todo
    template_name = 'todos/todo_confirm_delete.html'
    success_url = reverse_lazy('todo_list')


def toggle_resolved(request, pk):
    """Toggle the resolved status of a TODO item."""

    todo = get_object_or_404(Todo, pk=pk)
    todo.resolved = not todo.resolved
    todo.save()
    return redirect('todo_list')
