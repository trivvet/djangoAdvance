# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import Comment
from .forms import CommentForm

# Create your views here.

def comment_thread(request, cid):
    comment = Comment.objects.get(pk=cid)
    children = comment.children()
    # initial_data = {
    #     "content_type": comment.get_content_type,
    #     "object_id": instance.id
    # }
    form = CommentForm(
        # initial=initial_data
        )
    context = {
        'object': comment,
        'children': children,
        'form': form
    }

    return render(request, "comment_thread.html", context)
