from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import (
    TicketDeleteView,
    TicketEditView,
)


urlpatterns = [
    url(r'^(?P<ticket_id>[0-9]+)/$',
        login_required(TicketEditView.as_view()), name='ticket_edit'),
    url(r'^(?P<ticket_id>[0-9]+)/delete/$',
        login_required(TicketDeleteView.as_view()), name='ticket_delete'),
]
