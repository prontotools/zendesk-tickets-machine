# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.safestring import mark_safe

from django_tables2.utils import A
import django_tables2 as tables



from .models import Ticket
class TicketTable(tables.Table):
    check = tables.CheckBoxColumn(verbose_name=('Edit'), accessor='pk', orderable=False, attrs={'th__input': {'name': 'select_all'}})
    edit = tables.LinkColumn('ticket_edit', text='Edit', args=[A('pk')], orderable=False)
    delete = tables.LinkColumn('ticket_delete', text='Delete', args=[A('pk')], orderable=False)
    subject = tables.Column(orderable=False)
    comment = tables.Column(orderable=False)
    requester = tables.Column(default='-', orderable=False)
    created_by = tables.Column(default='-', orderable=False)
    assignee = tables.Column(default='-', orderable=False)
    group = tables.Column(orderable=False)
    ticket_type = tables.Column(default='-', orderable=False)
    due_at = tables.DateColumn(default='-', format='M d, Y', orderable=False, verbose_name=('Due Date'))
    priority = tables.Column(orderable=False)
    tags = tables.Column(default='-', orderable=False)
    private_comment = tables.Column(default='-', orderable=False)
    zendesk_ticket_id = tables.Column(default='-', orderable=False)

    class Meta:
        model = Ticket
        sequence = ('check', 'edit', 'delete' )
        exclude = ('id', 'board', 'is_active')
        attrs = {'class': 'table table-bordered table-condensed table-hover'}

    def render_zendesk_ticket_id(self, value):
        url = '<a href="%s/agent/tickets/%s" target="_blank">%s</a>' % (settings.ZENDESK_URL, value, value)
        return mark_safe(url)



