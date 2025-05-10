from django.db import models

class Property(models.Model):
    title = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    property_type = models.CharField(max_length=50)
    image = models.ImageField(upload_to='property_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # ✅ New field
    listed_on = models.DateTimeField(auto_now_add=True)
