from django.conf.urls import url

from .views import (
    TicketView,
    TicketDeleteView,
    TicketEditView,
    TicketResetView,
)


urlpatterns = [
    url(r'^$', TicketView.as_view(), name='tickets'),
    url(r'^reset/$',
        TicketResetView.as_view(), name='tickets_reset'),
    url(r'^(?P<ticket_id>[0-9]+)/$',
        TicketEditView.as_view(), name='ticket_edit'),
    url(r'^(?P<ticket_id>[0-9]+)/delete/$',
        TicketDeleteView.as_view(), name='ticket_delete'),
]
