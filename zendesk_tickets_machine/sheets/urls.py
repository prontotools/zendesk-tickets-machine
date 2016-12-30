from django.conf.urls import url

from .views import (
    SheetView,
)


urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$',
        SheetView.as_view(), name='sheet_view'),
]
