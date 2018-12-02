# -*- coding: utf-8 -*-
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
    organization = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    requester = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        Agent,
        null=True,
        blank=True,
        related_name='created_by',
        on_delete=models.SET_NULL,
    )
    assignee = models.ForeignKey(
        Agent,
        null=True,
        blank=True,
        related_name='assignee',
        on_delete=models.SET_NULL,
    )
    group = models.ForeignKey(
        AgentGroup,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    ticket_type = models.CharField(
        max_length=50,
        choices=TICKET_TYPE_CHOICES,
        null=True,
        blank=True,
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
    board = models.ForeignKey(
        Board,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    is_active = models.BooleanField(default=True)


@receiver(pre_save, sender=Ticket)
def create_zendesk_api_usage(sender, instance, **kwargs):
    try:
        current_ticket = Ticket.objects.get(id=instance.id)
        if not current_ticket.zendesk_ticket_id and instance.zendesk_ticket_id:
            TicketZendeskAPIUsage.objects.create(
                ticket_type=instance.ticket_type,
                requester=instance.requester,
                organization=instance.organization,
                priority=instance.priority,
                assignee=instance.assignee,
                board=instance.board
            )
    except:
        pass


class TicketZendeskAPIUsage(models.Model):
    ticket_type = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    requester = models.EmailField(max_length=300, null=True)
    organization = models.CharField(max_length=300, null=True)
    assignee = models.ForeignKey(
        Agent,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    board = models.ForeignKey(
        Board,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created = models.DateTimeField(auto_now_add=True)
