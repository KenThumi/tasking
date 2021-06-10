from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    phase = models.CharField(max_length=60)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tasks')
    

    def __str__(self):
        return self.title