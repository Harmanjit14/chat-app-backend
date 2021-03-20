from django.db import models
import uuid
from django.conf import settings
# Create your models here.


class ChatData(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    userA = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name="first_user")
    userB = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name="second_user")
    collection = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.id)
