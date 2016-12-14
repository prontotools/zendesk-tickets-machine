from django.db import models


class AgentGroup(models.Model):
    name = models.CharField(max_length=300)
    zendesk_group_id = models.CharField(max_length=100)

    def __str__(self):
        return self.name
