from __future__ import unicode_literals
import unicodedata

try:
    from urllib import quote_plus #python 2
except:
    pass

try:
    from urllib.parse import quote_plus #python 3
except: 
    pass

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import (
	Paginator, 
	EmptyPage, 
	PageNotAnInteger
	)
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from .forms import PostForm
from .models import Post
from .utils import get_read_time

from comments.forms import CommentForm
from comments.models import Comment

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
		
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		# message success
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form": form,
	}
	return render(request, "post_form.html", context)

'''
Created for Django Code Review
'''

from django.views.generic import DetailView

class PostDetailView(DetailView):
	template_name = 'post_detail.html' 
	
	def get_object(self, *args, **kwargs):
		slug = self.kwargs.get("slug")
		instance = get_object_or_404(Post, slug=slug)
		if instance.publish > timezone.now().date() or instance.draft:
			if not self.request.user.is_staff or not self.request.user.is_superuser:
				raise Http404
		return instance
	
	def get_context_data(self, *args, **kwargs):
		context = super(PostDetailView, self).get_context_data(
			*args, **kwargs
			)
		instance = context['object']
		context['share_string'] = quote_plus(
			instance.content.encode('utf8')
			)
		initial_data = {
		    "content_type": instance.get_content_type,
		    "object_id": instance.id
		}
		form = CommentForm(
			initial=initial_data
			)
		context['form'] = form
		return context

	def post(self, request, *args, **kwargs):
		instance = self.get_object()
		form = CommentForm(self.request.POST or None)
		if form.is_valid():
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
		return HttpResponseRedirect(
			new_comment.content_object.get_absolute_url())
	
# in urls.py --> PostDetailView.as_view() instead of post_detail


def post_detail(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)
	content_type = ContentType.objects.get_for_model(Post)
	obj_id = instance.id
	comments = Comment.objects.filter(content_type=content_type, 
		object_id=obj_id)
	context = {
		"title": instance.title,
		"instance": instance,
		"share_string": share_string,
		"comments": comments
	}
	return render(request, "post_detail.html", context)

def post_list(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 8) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
    
	context = {
		"object_list": queryset, 
		"title": "List",
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request, "post_list.html", context)





def post_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
	}
	return render(request, "post_form.html", context)



def post_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Successfully deleted")
	return redirect("posts:list")
