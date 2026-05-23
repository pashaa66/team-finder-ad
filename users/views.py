from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from team_finder.service import paginate

from .constants import USERS_PER_PAGE
from .forms import (
    CustomPasswordChangeForm,
    EditProfileForm,
    LoginForm,
    RegisterForm,
)
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect('projects:list')
    form = RegisterForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('projects:list')
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('projects:list')
    form = LoginForm(request.POST or None)
    if form.is_valid():
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
    if form.is_valid():
        form.save()
        return redirect('users:detail', user_id=request.user.pk)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    form = CustomPasswordChangeForm(
        user=request.user, data=request.POST or None
    )
    if form.is_valid():
        form.save()
        return redirect('users:detail', user_id=request.user.pk)
    return render(request, 'users/change_password.html', {'form': form})


def participants_list(request):
    qs = User.objects.filter(is_active=True).order_by('id')
    active_filter = None

    if request.user.is_authenticated:
        active_filter = request.GET.get('filter')
        me = request.user

        if active_filter == 'owners-of-favorite-projects':
            fav_ids = me.favorites.values_list('id', flat=True)
            qs = qs.filter(owned_projects__id__in=fav_ids).distinct()

        elif active_filter == 'owners-of-participating-projects':
            my_project_ids = me.participated_projects.values_list(
                'id', flat=True
            )
            qs = qs.filter(owned_projects__id__in=my_project_ids).distinct()

        elif active_filter == 'interested-in-my-projects':
            my_project_ids = me.owned_projects.values_list('id', flat=True)
            qs = qs.filter(favorites__id__in=my_project_ids).distinct()

        elif active_filter == 'participants-of-my-projects':
            my_project_ids = me.owned_projects.values_list('id', flat=True)
            qs = qs.filter(
                participated_projects__id__in=my_project_ids
            ).distinct()

    page_obj = paginate(qs, USERS_PER_PAGE, request)
    return render(
        request,
        'users/participants.html',
        {
            'page_obj': page_obj,
            'active_filter': active_filter,
        },
    )
