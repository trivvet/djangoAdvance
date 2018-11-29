from django.conf.urls import url

from .views import (
    comment_thread,
    )

urlpatterns = [
    url(r'^(?P<cid>[\w-]+)/$', comment_thread, name='thread'),
]