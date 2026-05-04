from django.urls import path
from . import views

urlpatterns=[
    path('',views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('create/', views.project_create, name='project_create'),
    path('update/<int:pk>/', views.project_update, name='project_update'),
    path('delete/<int:pk>/', views.project_delete, name='project_delete'),
]