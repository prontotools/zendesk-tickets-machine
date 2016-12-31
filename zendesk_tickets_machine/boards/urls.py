from django.conf.urls import url

from .views import (
    BoardView,
)


urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$',
        BoardView.as_view(), name='board_view'),
]
