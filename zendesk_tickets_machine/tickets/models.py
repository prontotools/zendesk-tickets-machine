from django.db import models


class Ticket(models.Model):
    subject = models.CharField(max_length=300)
    requester = models.CharField(max_length=100)
    assignee = models.CharField(max_length=100)
    ticket_type = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    tags = models.CharField(max_length=300)
