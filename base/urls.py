from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Recruiter (read-only)
    path('portfolio/', views.recruiter_home, name='recruiter_home'),

    # Contact (both roles)
    path('contact/', views.contact, name='contact'),

    # Admin dashboard
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),

    # Projects CRUD
    path('admin-panel/projects/add/', views.project_create, name='project_create'),
    path('admin-panel/projects/<int:pk>/edit/', views.project_update, name='project_update'),
    path('admin-panel/projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('admin-panel/projects/sync/', views.sync_github_projects, name='sync_github_projects'),

    # Experience
    path('admin-panel/experience/add/', views.add_experience, name='add_experience'),
    path('admin-panel/experience/<int:pk>/delete/', views.delete_experience, name='delete_experience'),
]