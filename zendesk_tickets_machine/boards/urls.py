from django.conf.urls import url

from .views import (
    BoardSingleView,
)


urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$',
        BoardSingleView.as_view(), name='board_single'),
]
