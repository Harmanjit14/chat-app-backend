from django.db import models
import uuid
from django.conf import settings
# Create your models here.


class LastLocation(models.Model):
    """Model to get users last known location to ftch nearby friends"""

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    city = models.CharField(null=True, max_length=255)
    state = models.CharField(null=True, max_length=255)
    country = models.CharField(null=True, max_length=255)
    date = models.DateTimeField(auto_now=True, editable=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.id
