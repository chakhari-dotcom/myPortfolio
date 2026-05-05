from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    technology = models.CharField(max_length=200, blank=True)
    github_link = models.URLField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Experience(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} at {self.company}"