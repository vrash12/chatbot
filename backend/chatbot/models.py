from django.db import models
from django.contrib.auth.models import User  # Import Django's User model
from cryptography.fernet import Fernet
from django.conf import settings
import base64

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Use Django's User model
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    encrypted_response = models.TextField(null=True, blank=True)
    intent = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Pending'), ('addressed', 'Addressed')], 
        default='pending'
    )
    addressed_by = models.ForeignKey('Staff', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.text

    def encrypt_response(self, response):
        fernet = Fernet(settings.ENCRYPTION_KEY)
        self.encrypted_response = fernet.encrypt(response.encode()).decode()
        self.save()

    def decrypt_response(self):
        fernet = Fernet(settings.ENCRYPTION_KEY)
        return fernet.decrypt(self.encrypted_response.encode()).decode()

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question

# Staff model to store information about the registrar's staff
class Staff(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    available = models.BooleanField(default=True)  # To check if staff is available for queries

    def __str__(self):
        return self.name

# Requestor model to store information about the users requesting information
class Requestor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, null=True, blank=True)
    student_id = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name
