from django.conf.urls import url

from .views import ZendeskTicketCreateView


urlpatterns = [
    url(r'^tickets/$', ZendeskTicketCreateView.as_view(),
        name='zendesk_ticket_create'),
]
