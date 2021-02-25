from django.db import models
from accounts.models import CustomUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=240, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="project/%Y/%m/", default="project/default.jpg", null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.BooleanField(_('Status'), default=False, help_text=_('Activated, allow to publish'))
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)

    def __str__(self):
        return {self.name}
