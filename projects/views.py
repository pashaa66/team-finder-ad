from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Project


def project_list(request):
    projects = Project.objects.select_related('owner').order_by('-created_at')
    paginator = Paginator(projects, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(
        request, 'projects/project_list.html', {'projects': page_obj}
    )
