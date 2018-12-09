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
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import UserLoginForm, UserRegisterForm

# Create your views here.

def login_view(request):
    form = UserLoginForm(request.POST or None)
    title = "Login Form"
    next = request.GET.get('next')
    if request.method == "POST":
        if form.is_valid():
            user = authenticate(request, 
                username=form.cleaned_data.get('username'), 
                password=form.cleaned_data.get('password'))
            login(request, user)
            messages.success(request, "You successfully logged in")
            if next:
                return redirect(next)
            return HttpResponseRedirect(reverse("posts:list"))

    context = {
        'form': form,
        'title': title
    }
    return render(request, "form.html", context)

def register_view(request):
    form = UserRegisterForm(request.POST or None)
    title = "Register Form"
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        new_user = authenticate(request,
            username=user.username, password=password)
        print new_user
        login(request, new_user)
        messages.success(request, "User is successfully created")
        return HttpResponseRedirect(reverse("posts:list"))
    context = {
        'form': form,
        'title': title
    }
    return render(request, "form.html", context)

def logout_view(request):
    logout(request)
    messages.success(request, "You logged out")
    return HttpResponseRedirect(reverse("home"))