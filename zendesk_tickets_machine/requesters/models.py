from django.db import models


class Requester(models.Model):
    email = models.CharField(max_length=300)
    zendesk_user_id = models.CharField(max_length=100)

    def __str__(self):
        return self.email
