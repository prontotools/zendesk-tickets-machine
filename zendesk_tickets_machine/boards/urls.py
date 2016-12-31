from django.conf.urls import url

from .views import (
    BoardView,
    BoardResetView,
    BoardSingleView,
    BoardZendeskTicketsCreateView,
)


urlpatterns = [
    url(r'^$', BoardView.as_view(), name='boards'),
    url(r'^(?P<slug>[\w-]+)/$',
        BoardSingleView.as_view(), name='board_single'),
    url(r'^(?P<slug>[\w-]+)/reset/$',
        BoardResetView.as_view(), name='board_reset'),
    url(r'^(?P<slug>[\w-]+)/tickets/$',
        BoardZendeskTicketsCreateView.as_view(), name='board_tickets_create'),
]
