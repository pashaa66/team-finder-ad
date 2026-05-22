from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CustomPasswordChangeForm,
    EditProfileForm,
    LoginForm,
    RegisterForm,
)
from .models import User


def register_view(request):
    form = RegisterForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('projects:list')
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('projects:list')
        form.add_error(None, 'Неверный имейл или пароль')
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('projects:list')


def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'users/user-details.html', {'user': user})


@login_required
def edit_profile(request):
    form = EditProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('users:detail', user_id=request.user.pk)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    form = CustomPasswordChangeForm(
        user=request.user, data=request.POST or None
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('users:detail', user_id=request.user.pk)
    return render(request, 'users/change_password.html', {'form': form})
