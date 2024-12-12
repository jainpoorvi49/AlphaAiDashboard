# app_name/models.py
from django.db import models

class NewUser(models.Model):
    user_id = models.CharField(max_length=255, unique=True)  # User ID
    password = models.CharField(max_length=255)  # Password
    mobile_number = models.CharField(max_length=15)  # Mobile Number
    broker_name = models.CharField(max_length=255)  # Broker Name
    # api_key = models.CharField(max_length=255)  # API Key
    # secret_key = models.CharField(max_length=255)  # Secret Key

    def __str__(self):
        return self.user_id
