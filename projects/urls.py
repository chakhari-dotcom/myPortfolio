from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('nouveau/', views.project_create, name='project_create'),
    path('modifier/<int:pk>/', views.project_update, name='project_update'),
    path('supprimer/<int:pk>/', views.project_delete, name='project_delete'),
]  