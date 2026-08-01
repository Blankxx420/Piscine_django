from django.db import models

class ModelTips(models.Model):
    content = models.TextField(null=False)
    author = models.CharField(null=False)
    date_creation = models.DateTimeField(auto_now=True)