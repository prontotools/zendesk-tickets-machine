from django.db import models


class Ticket(models.Model):
    subject = models.CharField(max_length=300)
    comment = models.CharField(max_length=500)
    requester = models.CharField(max_length=100)
    requester_id = models.CharField(max_length=50)
    assignee = models.CharField(max_length=100)
    assignee_id = models.CharField(max_length=50)
    ticket_type = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    tags = models.CharField(max_length=300)
