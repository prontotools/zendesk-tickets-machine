from django.conf.urls import url

from .views import (
    TicketDeleteView,
    TicketEditView,
)


urlpatterns = [
    url(r'^(?P<ticket_id>[0-9]+)/$',
        TicketEditView.as_view(), name='ticket_edit'),
    url(r'^(?P<ticket_id>[0-9]+)/delete/$',
        TicketDeleteView.as_view(), name='ticket_delete'),
]
