from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class ModelTips(models.Model):

    content = models.TextField(null=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='tips_posted',
        null=False
    )
    date_creation = models.DateTimeField(auto_now=True)

    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='upvoted_tips', blank=True)
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='downvoted_tips', blank=True)

    class Meta:
        permissions = [("allow_downvotes", "allow downvote for tips")]

    @property
    def total_upvotes(self):
        return self.upvotes.count()

    @property
    def total_downvotes(self):
        return self.downvotes.count()

class CustomUser(AbstractUser):

    reputation = models.IntegerField(default=0)

    def can_downvote(self, tip):
        if self == tip.author:
            return True
        return bool(self.has_perm('ex.allow_downvotes') or self.reputation >= 15)

    def can_delete(self, tip):
        if self == tip.author:
            return True
        return bool(self.has_perm('ex.delete_modeltips') or self.reputation >= 30)

    def update_reputation(self):
        score = 0
        for tip in self.tips_posted.all(): # Assurez-vous que related_name='tips_posted' est dans votre modèle Tip
            score += (tip.upvotes.count() * 5)
            score -= (tip.downvotes.count() * 2)
        self.reputation = score
        self.save()