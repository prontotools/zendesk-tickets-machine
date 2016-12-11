from django.conf.urls import url

from .views import TicketView, TicketNewView


urlpatterns = [
    url(r'^$', TicketView.as_view(), name='tickets'),
    url(r'^(?P<ticket_id>[0-9]+)/$',
        TicketNewView.as_view(), name='tickets_new'),
]
