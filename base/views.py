from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import Project, Category

def home(request):
    projects = Project.objects.all() 
    return render(request, 'base/home.html', {'projects': projects})

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




