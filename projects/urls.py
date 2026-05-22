from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.project_list, name='list'),
    path('<int:project_id>/', views.project_detail, name='detail'),
    path(
        '<int:project_id>/complete/', views.complete_project, name='complete'
    ),
    path(
        '<int:project_id>/toggle-participate/',
        views.toggle_participate,
        name='toggle_participate',
    ),
]
