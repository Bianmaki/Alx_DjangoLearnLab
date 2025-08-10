from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from .models import Book
from .forms import BookForm
from .forms import BookSearchForm
from .forms import ExampleForm

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def example_form_view(request):
    """
    Handles ExampleForm submissions securely.
    Demonstrates CSRF protection and safe ORM queries.
    """
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Cleaned data is safe to use
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Example: you could log it, send email, or save to DB
            # For now, just redirect to a success page
            return redirect('form_success')
    else:
        form = ExampleForm()

    return render(request, 'bookshelf/form_example.html', {'form': form})


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_search(request):
    form = BookSearchForm(request.GET or None)
    qs = Book.objects.none()
    if form.is_valid():
        q = form.cleaned_data.get('q')
        if q:
            # Use ORM and parameterized lookup — avoids SQL injection
            qs = Book.objects.filter(
                Q(title__icontains=q) | Q(author__name__icontains=q)
            )
    return render(request, 'bookshelf/book_list.html', {'form': form, 'books': qs})

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def search_books(request):
    q = request.GET.get('q', '').strip()
    if q:
        books = Book.objects.filter(Q(title__icontains=q) | Q(author__icontains=q))
    else:
        books = Book.objects.none()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/add_book.html', {'form': form})


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/edit_book.html', {'form': form})


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/delete_book.html', {'book': book})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def form_success(request):
    """
    Simple success page after form submission.
    """
    return render(request, 'bookshelf/form_success.html')