from django.db import models

from agents.models import Agent
from agent_groups.models import AgentGroup
from boards.models import Board


class Ticket(models.Model):
    TICKET_TYPE_CHOICES = (
        ('question', 'Question'),
        ('incident', 'Incident'),
        ('problem', 'Problem'),
        ('task', 'Task'),
    )

    PRIORITY_TYPE_CHOICES = (
        ('high', 'High'),
        ('urgent', 'Urgent'),
        ('normal', 'Normal'),
        ('low', 'Low'),
    )

    subject = models.CharField(max_length=300)
    comment = models.TextField()
    requester = models.CharField(max_length=100)
    assignee = models.ForeignKey(Agent)
    group = models.ForeignKey(AgentGroup)
    ticket_type = models.CharField(max_length=50, choices=TICKET_TYPE_CHOICES)
    priority = models.CharField(max_length=50, choices=PRIORITY_TYPE_CHOICES)
    tags = models.CharField(max_length=300, null=True, blank=True)
    private_comment = models.TextField(null=True, blank=True)
    zendesk_ticket_id = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    board = models.ForeignKey(Board)

    def save(self, *args, **kwargs):
        super(Ticket, self).save(*args, **kwargs)

        if self.zendesk_ticket_id:
            TicketZendeskAPIUsage.objects.create(
                ticket_type=self.ticket_type,
                priority=self.priority,
                assignee=self.assignee,
                board=self.board
            )


class TicketZendeskAPIUsage(models.Model):
    ticket_type = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    assignee = models.ForeignKey(Agent)
    board = models.ForeignKey(Board)
    created = models.DateTimeField(auto_now_add=True)
