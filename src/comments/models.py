# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from posts.models import Post

# Create your models here.

class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(Post)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, 
            object_id=obj_id)
        return qs

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    #post =  models.ForeignKey(Post)

    content_type = models.ForeignKey(ContentType, 
        on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    content = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(u"Comment about {}".format(self.user))

    def __str__(self):
        return str(u"Comment about {}".format(self.user))