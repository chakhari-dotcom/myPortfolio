import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import Project, Category


def home(request):
    projects = Project.objects.all()
    return render(request, 'base/home.html', {'projects': projects})


def get_github_repos(username):
    url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(request, timeout=10) as response:
            return json.load(response)
    except (HTTPError, URLError, ValueError) as error:
        raise RuntimeError(f"Unable to fetch GitHub repositories: {error}")


def get_category_name(language):
    if not language:
        return "Other"
    language = language.lower()
    if language in {"python"}:
        return "Python"
    if language in {"javascript", "typescript", "php", "html", "css"}:
        return "Web Development"
    if language in {"java"}:
        return "Mobile Development"
    return "Other"


def sync_github_projects():
    repos = get_github_repos("chakhari-dotcom")
    synced_titles = []

    for repo in repos:
        title = repo.get("name", "").strip()
        if not title:
            continue

        description = repo.get("description") or ""
        technology = repo.get("language") or "Unknown"
        github_link = repo.get("html_url", "")
        category_name = get_category_name(repo.get("language"))
        category, _ = Category.objects.get_or_create(name=category_name)

        Project.objects.update_or_create(
            title=title,
            defaults={
                "description": description,
                "technology": technology,
                "category": category,
                "github_link": github_link,
            },
        )
        synced_titles.append(title)

    Project.objects.exclude(title__in=synced_titles).delete()
    return len(synced_titles)


def sync_github_projects_view(request):
    try:
        count = sync_github_projects()
        messages.success(request, f"Synced {count} GitHub project(s).")
    except Exception as error:
        messages.error(request, f"GitHub sync failed: {error}")
    return redirect('home')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        company = request.POST.get('company', '')
        
       
        email_subject = f"Portfolio Contact: {subject}"
        email_message = f"""
New message from your portfolio website!

From: {name}
Email: {email}
Company: {company if company else 'Not specified'}

Subject: {subject}

Message:
{message}
"""
        
        
        try:
            send_mail(
                email_subject,
                email_message,
                email,  
                ['fatmaa.chakhari@gmail.com'],  
                fail_silently=False,
            )
            messages.success(request, 'Thank you for your message! I will get back to you soon.')
        except Exception as e:
            print(f"Error sending email: {e}")
            messages.error(request, 'Sorry for the inconvenience. Your message could not be sent at this time. Please try again later.')
        
        return redirect('contact')
    
    return render(request, 'base/contact.html')

def project_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        technology = request.POST.get('technology')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        Project.objects.create(title=title, description=description, technology=technology, category=category)
        return redirect('home')
    categories = Category.objects.all()
    return render(request, 'base/project_form.html', {'categories': categories, 'action': 'Créer'})

def project_update(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.description = request.POST.get('description')
        project.technology = request.POST.get('technology')
        project.category = Category.objects.get(id=request.POST.get('category'))
        project.save()
        return redirect('home')
    categories = Category.objects.all()
    return render(request, 'base/project_form.html', {'project': project, 'categories': categories, 'action': 'Modifier'})

def project_delete(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('home')
    return render(request, 'base/project_confirm_delete.html', {'project': project})




