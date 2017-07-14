# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.safestring import mark_safe

import django_tables2 as tables

from .models import Ticket

TEMPLATE = '<a href="{% url "ticket_edit" record.id %}" ' \
    'class="tbl_icon edit"><i class="fa fa-pencil modal-button" ' \
    'data-target="#modal-edit-ticket"></i></a>&nbsp;' \
    '<a href="{% url "ticket_delete" record.id %}" ' \
    'class="tbl_icon_delete"><i class="fa fa-trash-o"></i></a>'


class TicketTable(tables.Table):
    check = tables.CheckBoxColumn(
        verbose_name=('Edit'),
        accessor='pk',
        orderable=False,
        attrs={
            'th__input': {
                'name': 'select_all'
                }
            }
    )
    subject = tables.Column(orderable=False)
    comment = tables.Column(orderable=False)
    requester = tables.Column(default='-', orderable=True)
    created_by = tables.Column(default='-', orderable=False)
    assignee = tables.Column(default='-', orderable=False)
    group = tables.Column(orderable=False)
    ticket_type = tables.Column(default='-', orderable=False)
    due_at = tables.DateColumn(
        default='-',
        format='M d, Y',
        orderable=False,
        verbose_name=('Due Date'))
    priority = tables.Column(orderable=False)
    tags = tables.Column(default='-', orderable=False)
    private_comment = tables.Column(default='-', orderable=False)
    zendesk_ticket_id = tables.Column(default='-', orderable=False)
    manage = tables.TemplateColumn(TEMPLATE, orderable=False)

    class Meta:
        model = Ticket
        sequence = ('check',)
        exclude = ('id', 'board', 'is_active')
        attrs = {'class': 'table  table-hover'}

    def render_zendesk_ticket_id(self, value):
        url = '<a href="%s/agent/tickets/%s" target="_blank">%s</a>' \
            % (settings.ZENDESK_URL, value, value)
        return mark_safe(url)
