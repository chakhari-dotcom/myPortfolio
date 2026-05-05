from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Project, Experience
import requests

# ── helpers ───────────────────────────────────────────────────────────────────
def is_admin(user):
    return user.is_superuser or user.is_staff

# ── Auth ──────────────────────────────────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard' if is_admin(request.user) else 'recruiter_home')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('admin_dashboard' if is_admin(user) else 'recruiter_home')
        messages.error(request, 'Invalid credentials.')
    return render(request, 'base/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# ── Recruiter (read-only) ─────────────────────────────────────────────────────
@login_required(login_url='login')
def recruiter_home(request):
    return render(request, 'base/recruiter_home.html', {
        'projects': Project.objects.all(),
        'experiences': Experience.objects.all(),
    })

# ── Contact ───────────────────────────────────────────────────────────────────
@login_required(login_url='login')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject', 'Portfolio Contact')
        message = request.POST.get('message')
        try:
            send_mail(
                subject=f'{subject} — from {name}',
                message=f'From: {name} <{email}>\n\n{message}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
            )
            messages.success(request, 'Message sent successfully!')
        except Exception as e:
            messages.error(request, f'Failed to send message: {e}')
        return redirect('contact')
    return render(request, 'base/contact.html')

# ── Admin: dashboard ──────────────────────────────────────────────────────────
@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def admin_dashboard(request):
    return render(request, 'base/admin_dashboard.html', {
        'projects': Project.objects.all(),
        'experiences': Experience.objects.all(),
    })

# ── Admin: project CRUD ───────────────────────────────────────────────────────
@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def project_create(request):
    if request.method == 'POST':
        Project.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description', ''),
            category=request.POST.get('category', ''),
            technology=request.POST.get('technology', ''),
            github_link=request.POST.get('github_link', ''),
        )
        messages.success(request, 'Project created!')
        return redirect('admin_dashboard')
    return render(request, 'base/project_form.html', {'action': 'Create'})

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.description = request.POST.get('description', '')
        project.category = request.POST.get('category', '')
        project.technology = request.POST.get('technology', '')
        project.github_link = request.POST.get('github_link', '')
        project.save()
        messages.success(request, 'Project updated!')
        return redirect('admin_dashboard')
    return render(request, 'base/project_form.html', {'action': 'Update', 'project': project})

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted.')
        return redirect('admin_dashboard')
    return render(request, 'base/project_confirm_delete.html', {'project': project})

# ── Admin: sync GitHub ────────────────────────────────────────────────────────
@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def sync_github_projects(request):
    try:
        response = requests.get('https://api.github.com/users/chakhari-dotcom/repos', timeout=10)
        repos = response.json()
        count = 0
        for repo in repos:
            if not repo.get('fork'):
                obj, created = Project.objects.get_or_create(
                    title=repo['name'],
                    defaults={
                        'description': repo.get('description') or '',
                        'github_link': repo.get('html_url', ''),
                        'category': 'Web Development',
                        'technology': repo.get('language') or '',
                    }
                )
                if created:
                    count += 1
        messages.success(request, f'Synced {count} new project(s) from GitHub.')
    except Exception as e:
        messages.error(request, f'GitHub sync failed: {e}')
    return redirect('admin_dashboard')

# ── Admin: experience ─────────────────────────────────────────────────────────
@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def add_experience(request):
    if request.method == 'POST':
        Experience.objects.create(
            title=request.POST.get('title'),
            company=request.POST.get('company'),
            location=request.POST.get('location', ''),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date') or None,
            description=request.POST.get('description', ''),
            is_current=request.POST.get('is_current') == 'on',
        )
        messages.success(request, 'Experience added!')
        return redirect('admin_dashboard')
    return render(request, 'base/experience_form.html')

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def delete_experience(request, pk):
    exp = get_object_or_404(Experience, pk=pk)
    if request.method == 'POST':
        exp.delete()
        messages.success(request, 'Experience deleted.')
    return redirect('admin_dashboard')