from django.db import models

class Contact(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.full_name
    
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True, null=True)  # Optional
    image = models.ImageField(upload_to='feedback_images/')
    quote = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class PortfolioProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='portfolio_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title