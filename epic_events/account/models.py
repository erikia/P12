from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Account(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=250)
    phoneNumber = PhoneNumberField(unique=True, null=False, blank=False)
    secondPhoneNumber = PhoneNumberField(null=True, blank=True)
    company = models.CharField(max_length=50)
    status = models.CharField(max_length=12, choices=[("Active", "Active"), ("Not Active", "Not Active")])
    assignee = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    edited_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company