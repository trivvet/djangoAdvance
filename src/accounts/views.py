# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
    )
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import UserLoginForm

# Create your views here.

def login_view(request):
    form = UserLoginForm(request.POST or None)
    title = "Login Form"
    if request.method == "POST":
        if form.is_valid():
            user = authenticate(request, 
                username=form.cleaned_data.get('username'), 
                password=form.cleaned_data.get('password'))
            login(request, user)
            messages.success(request, "You successfully logged in")
            return HttpResponseRedirect(reverse("posts:list"))

    context = {
        'form': form,
        'title': title
    }
    return render(request, "form.html", context)

def register_view(request):
    return render(request, "form.html", {})

def logout_view(request):
    logout(request)
    messages.success(request, "You logged out")
    return HttpResponseRedirect(reverse("home"))