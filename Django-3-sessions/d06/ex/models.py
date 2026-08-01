from django.contrib.auth.models import User
from django.db import models


class ModelTips(models.Model):

    content = models.TextField(null=False)
    author = models.CharField(null=False)
    date_creation = models.DateTimeField(auto_now=True)

    upvotes = models.ManyToManyField(User, related_name='upvoted_tips', blank=True)
    downvotes = models.ManyToManyField(User, related_name='downvoted_tips', blank=True)


    @property
    def total_upvotes(self):
        return self.upvotes.count()

    @property
    def total_downvotes(self):
        return self.downvotes.count()
