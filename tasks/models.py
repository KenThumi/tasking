from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Phase(models.Model):
    title = models.CharField(max_length=60)
    

    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    phase = models.ForeignKey(Phase,on_delete=models.CASCADE,related_name='tasks', default=1)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tasks')
    


    class Meta:
        ordering = ["-pk"]


    def __str__(self):
        return self.title


class Challege(models.Model):
    description = models.TextField()
    task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name='challenges')



    class Meta:
        ordering = ["-pk"]


    def __str__(self):
        return self.title
