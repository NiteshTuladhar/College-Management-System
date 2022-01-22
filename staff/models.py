from django.db import models
from Accounts.models import Account
# Create your models here.

class Staff(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

