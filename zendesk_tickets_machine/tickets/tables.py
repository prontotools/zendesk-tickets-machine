import django_tables2 as tables
from django_tables2.utils import A

from .models import Ticket
class TicketTable(tables.Table):
    check = tables.CheckBoxColumn(verbose_name=('Edit'), accessor='pk', orderable=False)
    edit = tables.LinkColumn('ticket_edit', text='Edit', args=[A('pk')], orderable=False)
    delete = tables.LinkColumn('ticket_delete', text='Delete', args=[A('pk')], orderable=False)
    due_at = tables.DateColumn()
    
    class Meta:
        model = Ticket
        sequence = ('check', 'edit', 'delete' )
        exclude = ('id', 'board', 'is_active')
        attrs = {'class': 'table table-bordered table-condensed table-hover'}



