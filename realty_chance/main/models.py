from django.db import models
from django.contrib.auth.models import User



class ListedProperty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    property_type = models.CharField(max_length=50)
    image = models.ImageField(upload_to='property_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    listed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Property(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('owner', 'Owner'),
        ('buyer', 'Buyer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
