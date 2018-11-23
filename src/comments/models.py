# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from posts.models import Post

# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    post =  models.ForeignKey(Post)
    content = models.TextField(blank=False, null=False)
    timestamp = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return str(u"Comment about {}".format(self.post))

    def __str__(self):
        return str(u"Comment about {}".format(self.post))