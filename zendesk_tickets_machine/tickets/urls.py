from django.conf.urls import url

from .views import TicketView


urlpatterns = [
    url(r'^$', TicketView.as_view(), name='tickets'),
]
