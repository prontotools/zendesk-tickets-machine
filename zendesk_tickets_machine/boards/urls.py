from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import (
    BoardView,
    BoardRequestersResetView,
    BoardResetView,
    BoardSingleView,
    BoardZendeskTicketsCreateView,
)


urlpatterns = [
    url(r'^$', login_required(BoardView.as_view()), name='boards'),
    url(r'^(?P<slug>[\w-]+)/$',
        login_required(BoardSingleView.as_view()), name='board_single'),
    url(r'^(?P<slug>[\w-]+)/requesters/reset/$',
        login_required(BoardRequestersResetView.as_view()), name='board_requesters_reset'),
    url(r'^(?P<slug>[\w-]+)/reset/$',
        login_required(BoardResetView.as_view()), name='board_reset'),
    url(r'^(?P<slug>[\w-]+)/tickets/$',
        login_required(BoardZendeskTicketsCreateView.as_view()),
        name='board_tickets_create'),
]
