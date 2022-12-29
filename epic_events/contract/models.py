from django.conf import settings
from django.db import models

from account.models import Account


class Contract(models.Model):
    account = models.ForeignKey(to=Account, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=12, choices=[("Signed", "Signed"), ("Not Signed", "Not Signed")])
    assignee = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    signature_time = models.DateTimeField(null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    edited_time = models.DateTimeField(auto_now=True)
    amount = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.account} contract {self.id}"