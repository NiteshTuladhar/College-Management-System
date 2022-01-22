from django.db import models
from Accounts.models import Account

# Create your models here.
class Teacher(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    experience = models.IntegerField(null=True, blank=True)
    teacher_id = models.CharField(blank=True, null=True, max_length=50)


    def __str__(self):
        return self.user.full_name
