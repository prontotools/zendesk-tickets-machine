from django.conf.urls import url

from .views import TicketView, TicketEditView


urlpatterns = [
    url(r'^$', TicketView.as_view(), name='tickets'),
    url(r'^(?P<ticket_id>[0-9]+)/$',
        TicketEditView.as_view(), name='ticket_edit'),
]
