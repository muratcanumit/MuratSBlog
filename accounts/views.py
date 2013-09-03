from blogArticles.models import Post, Comment
from accounts.models import UserProfile

from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render

from django import template
from django.template.defaulttags import register
from django.template import RequestContext
from django.template import Context, loader

from django.contrib.contenttypes.models import ContentType


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from accounts.forms import (LoginForm, RegisterForm,
                            UserProfileForm, EmailChangeForm,
                            PasswordChangeForm, AccountDisableForm)

from django.contrib import messages
# from tasks import sendmail


@login_required
def homepage(request):
    latest_post_list = Post.objects.all().order_by('-created_on')[:10]
    return render(request, 'blogArticles/homepage.html',
                  {'latest_post_list': latest_post_list})


def loginPage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username,
                                password=password
                                )

            if user is not None:
                if user.accounts.is_verified is False:
                    messages.error(request,
                                   'Verify your account with activation key.')
                elif user.is_active():
                    login(request, user)
                    messages.success(request, 'Logged in Successful.')
                    return HttpResponseRedirect(reverse('homepage'))
                else:
                    messages.error(request,
                                   'Login Failed. This account is inactive.')
                    return HttpResponseRedirect(reverse('login'))
            else:
                messages.error(
                    request,
                    'Login Failed. Wrong Username or Password. Try Again.'
                )
                return HttpResponseRedirect(reverse('login'))
    else:
        form = LoginForm
    return render(request, 'login.html', {'form': form})


@login_required
def logoutPage(request):
    logout(request)
    return HttpResponseRedirect('index')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.create_user(user)
            user.is_active = False
            user.save()
            messages.success(request, 'Successfully Registered.')
        else:
            messages.error(request, 'Fields have to be correctly filled.')
            return HttpResponseRedirect(reverse('register'))
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def editProfile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user = request.user.get_profile()
            user_avatar = request.FILES.get("user_avatar")
            if user_avatar is not None:
                user.user_avatar.delete()
            user.user_avatar = user_avatar
            user_avatar.save()
            messages.success(request, 'Your Avatar has changed.')
            user.save()
            messages.success(request, 'Changes are done.')
        else:
            messages.error(request, 'Something is wrong.')
            return HttpResponseRedirect(reverse('editprofile'))
    else:
        form = UserProfileForm()
    return render(request, 'editprofile.html', {'form': form})


@login_required
def emailChange(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST)
    if form.is_valid():
        user = request.user.get_profile()
        user.email = form.save()
        user.is_verified = False
        user.is_active = False
        user.save()
        messages.success(request, 'Email has changed.Verification is sent.')
        return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Process failed. Try again.')
        form = EmailChangeForm()
    return render(request, 'emailchange.html', {'form': form})


@login_required
def passwordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
    if form.is_valid():
        user = request.user.get_profile()
        form.save()
        messages.success(request, 'Email has changed.Verification is sent.')
        return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Process failed. Try again.')
        form = PasswordChangeForm()
    return render(request, 'passwordchange.html', {'form': form})


@login_required
def disableAccount(request):
    user = User.objects.get(request.user)

