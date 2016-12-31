from django.conf.urls import url

from .views import (
    BoardView,
    BoardResetView,
    BoardSingleView,
)


urlpatterns = [
    url(r'^$', BoardView.as_view(), name='boards'),
    url(r'^(?P<slug>[\w-]+)/$',
        BoardSingleView.as_view(), name='board_single'),
    url(r'^(?P<slug>[\w-]+)/reset/$',
        BoardResetView.as_view(), name='board_reset'),
]
