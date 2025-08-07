from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Library
from .models import Book


def is_admin(user):
    return user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.userprofile.role == 'Librarian'

def is_member(user):
    return user.userprofile.role == 'Member'


def list_books(request):  
    books = Book.objects.all()
    all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'relationship_app/register.html'

class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'


from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render

def is_admin(user):
    return hasattr(user,'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

def member_view(request):
    return render(request, 'relationship_app/member_view.html')

