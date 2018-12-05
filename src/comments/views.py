# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import DeleteView

from .models import Comment
from .forms import CommentForm

# Create your views here.

def comment_thread(request, cid):
    comment = Comment.objects.get(pk=cid)
    children = comment.children()
    initial_data = {
        "content_type": comment.get_content_type,
        "object_id":  comment.id
    }
    form = CommentForm(
        request.POST or None,
        initial=initial_data
        )
    if request.method == "POST" and form.is_valid():
        data = {}
        c_type = form.cleaned_data.get("content_type")
        parent_id = request.POST.get('parent_id')
        data['content_type'] = ContentType.objects.get(model=c_type)
        data['object_id'] = form.cleaned_data.get("object_id")
        data['content'] = form.cleaned_data.get("content")
        data['user'] = request.user
        if parent_id:
            data['parent'] = Comment.objects.get(pk=parent_id)
        new_comment = Comment(**data)
        new_comment.save()
        messages.success(request, "Comment successfully added!")
        return HttpResponseRedirect(
            new_comment.content_object.get_absolute_url())

    context = {
        'object': comment,
        'children': children,
        'form': form
    }

    return render(request, "comment_thread.html", context)

class CommentDelete(DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'

    def get_success_url(self):
        if self.object.parent:
            return self.object.parent.get_absolute_url()
        else:
            return self.object.content_object.get_absolute_url()

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        success_message = "{} was deleted successfully.".format(
            comment)
        messages.success(self.request, success_message)
        return super(CommentDelete, self).delete(request, *args, **kwargs)
