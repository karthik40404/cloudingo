from django.db import models
from django.contrib.auth.models import User

class UserFile(models.Model):
    CATEGORY_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('file', 'File'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files', default=1)  # Default user with ID 1
    file = models.FileField(upload_to='uploads/')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.category})"
