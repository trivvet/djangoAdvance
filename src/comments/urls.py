from django.conf.urls import url

from .views import (
    comment_thread,
    CommentDelete
    )

urlpatterns = [
    url(r'^(?P<cid>[\w-]+)/$', comment_thread, name='thread'),
    url(r'^(?P<pk>[0-9]+)/delete/$', CommentDelete.as_view(), 
        name="delete"),
]