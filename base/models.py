from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    github_link = models.URLField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True) 