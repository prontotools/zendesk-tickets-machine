from django.conf.urls import url

from .views import ZendeskTicketsCreateView


urlpatterns = [
    url(r'^tickets/$', ZendeskTicketsCreateView.as_view(),
        name='zendesk_tickets_create'),
]
