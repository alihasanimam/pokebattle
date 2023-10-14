from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Battle(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    challenger = models.CharField(blank=False, null=False, max_length=64)
    defender = models.TextField(blank=False, null=False, max_length=64)
    winner = models.TextField(blank=False, null=False, max_length=64)
    user = models.ForeignKey(User, related_name='battles', on_delete=models.CASCADE)
    data = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)