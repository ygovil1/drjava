from django.db import models
from django.conf import settings

# Create your models here.

class Face(models.Model):
    name = models.CharField(max_length=160, primary_key=True)
    creation = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.name