import django_tables2 as tables
from django_tables2.utils import A
from django.conf import settings
from django.utils.safestring import mark_safe

from .models import Ticket
class TicketTable(tables.Table):
    check = tables.CheckBoxColumn(verbose_name=('Edit'), accessor='pk', orderable=False, attrs={'th__input': {'name': 'select_all'}})
    edit = tables.LinkColumn('ticket_edit', text='Edit', args=[A('pk')], orderable=False)
    delete = tables.LinkColumn('ticket_delete', text='Delete', args=[A('pk')], orderable=False)
    due_at = tables.DateColumn(format='M d, Y')
    zendesk_ticket_id = tables.Column()

    class Meta:
        model = Ticket
        sequence = ('check', 'edit', 'delete' )
        exclude = ('id', 'board', 'is_active')
        attrs = {'class': 'table table-bordered table-condensed table-hover'}

    def render_zendesk_ticket_id(self, value):
        url = '<a href="%s/agent/tickets/%s" target="_blank">%s</a>' % (settings.ZENDESK_URL, value, value)
        return mark_safe(url)



