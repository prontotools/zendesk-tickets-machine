from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

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
    created_by = models.ForeignKey(
        Agent, null=True, blank=True, related_name='created_by')
    assignee = models.ForeignKey(
        Agent, null=True, blank=True, related_name='assignee')
    group = models.ForeignKey(AgentGroup)
    ticket_type = models.CharField(
        max_length=50,
        choices=TICKET_TYPE_CHOICES,
        null=True,
        blank=True
    )
    due_at = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=50, choices=PRIORITY_TYPE_CHOICES)
    tags = models.CharField(max_length=300, null=True, blank=True)
    private_comment = models.TextField(null=True, blank=True)
    zendesk_ticket_id = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    board = models.ForeignKey(Board)
    is_active = models.BooleanField(default=True)

    def link(self):
        return format_html('<a href="{}">Edit</a> | <a href="{}">Delete</a>' , '#', '#')


@receiver(pre_save, sender=Ticket)
def create_zendesk_api_usage(sender, instance, **kwargs):
    try:
        current_ticket = Ticket.objects.get(id=instance.id)
        if not current_ticket.zendesk_ticket_id and instance.zendesk_ticket_id:
            TicketZendeskAPIUsage.objects.create(
                ticket_type=instance.ticket_type,
                priority=instance.priority,
                assignee=instance.assignee,
                board=instance.board
            )
    except:
        pass


class TicketZendeskAPIUsage(models.Model):
    ticket_type = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    assignee = models.ForeignKey(Agent)
    board = models.ForeignKey(Board)
    created = models.DateTimeField(auto_now_add=True)
