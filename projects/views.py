from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ProjectForm
from .models import Project


def project_list(request):
    projects = Project.objects.select_related('owner').order_by('-created_at')
    paginator = Paginator(projects, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(
        request, 'projects/project_list.html', {'projects': page_obj}
    )


def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(
        request, 'projects/project-details.html', {'project': project}
    )


@login_required
@require_POST
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user

    if user == project.owner:
        return JsonResponse(
            {'status': 'error', 'message': 'Owner cannot leave own project'},
            status=400,
        )

    if user in project.participants.all():
        project.participants.remove(user)
    else:
        project.participants.add(user)

    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def complete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if project.owner != request.user or project.status != 'open':
        return JsonResponse(
            {
                'status': 'error',
                'message': 'Forbidden or project already closed',
            },
            status=400,
        )

    project.status = 'closed'
    project.save()

    return JsonResponse({'status': 'ok', 'project_status': 'closed'})


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect('projects:list')
    return render(
        request,
        'projects/create-project.html',
        {'form': form, 'is_edit': False},
    )


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('projects:list')
    return render(
        request,
        'projects/create-project.html',
        {'form': form, 'is_edit': True},
    )
