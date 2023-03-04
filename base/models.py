from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False) 
    created = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        if self.title:
            return self.title
        else:
            return "Przypomnienie bez nazwy"
    
    class Meta:
        ordering = ['-created']

    