from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import RegisterForm, ProfileForm


class BlogLoginView(LoginView):
    template_name = "blog/auth/login.html"


class BlogLogoutView(LogoutView):
    next_page = reverse_lazy("blog:login")


def register(request):
    if request.user.is_authenticated:
        return redirect("blog:profile")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully. Welcome!")
            return redirect("blog:profile")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()
    return render(request, "blog/auth/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile,
                           initial={
                               "first_name": request.user.first_name,
                               "last_name": request.user.last_name,
                               "email": request.user.email,
                           })
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, "Profile updated.")
            return redirect("blog:profile")
        messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=request.user.profile, initial={
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
        })
    return render(request, "blog/auth/profile.html", {"form": form})

