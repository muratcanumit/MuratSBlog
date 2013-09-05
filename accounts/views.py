import datetime
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext as _

from blogArticles.models import Post, Comment
from accounts.models import UserProfile
from accounts.forms import (LoginForm, RegisterForm,
                            UserProfileForm, EmailChangeForm,
                            PasswordChangeForm)
from blogArticles.forms import PostAddForm


@login_required
def homepage(request):
    latest_post_list = Post.objects.all().order_by('-created_on')[:10]
    users = User.objects.all()
    return render(request, 'blogArticles/homepage.html',
                  {'latest_post_list': latest_post_list, 'users': users})


def detailed(request, post_id):
    p = get_object_or_404(Post, pk=post_id)
    ct_post = ContentType.objects.get_for_model(Post)
    post_comments = Comment.objects.filter(entity=post_id).order_by(
        'created_on').filter(content_type=ct_post)

    ct_comment = ContentType.objects.get_for_model(Comment)
    comment_list = Comment.objects.filter(entity=post_id).order_by(
        'created_on').filter(content_type=ct_comment)
    # return redirect(request, reverse('urls_name'))
    return render(request, 'blogArticles/postdetailed.html',
                  {'post': p, 'comment_list': comment_list,
                   'post_comment_list': post_comments})


def loginPage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(username=username,
                                password=password
                                )

            if user is not None:
                if user.is_active is False:
                    messages.error(request,
                                   _('Verify account with activation key.'))
                    return HttpResponseRedirect(reverse('login'))
                elif user.is_active is True:
                    login(request, user)
                    messages.success(request, _('Logged in Successful.'))
                    return HttpResponseRedirect(reverse('homepage'))

            else:
                messages.error(
                    request,
                    _('Login Failed. Invalid Username or Password. Try Again.')
                )
                return HttpResponseRedirect(reverse('login'))
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logoutPage(request):
    logout(request)
    return HttpResponseRedirect('/')


def registerPage(request):
    messages.info(request, _('Your user name will automatically be email.'
                             'You need to change your username after login.'))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.username = user.email
            user.save()
            messages.success(request, _('Successfully Registered.'))
            return HttpResponseRedirect(reverse('login'))
        else:
            messages.error(request, _('Fields have to be correctly filled.'))
            return HttpResponseRedirect(reverse('register'))
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def editProfile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                userprofile = user.userprofile
            except UserProfile.DoesNotExist:
                userprofile = form.instance

            userprofile.user = user
            userprofile.is_verified = True
            userprofile.act_key = "1111"
            userprofile.exp_key = datetime.datetime.now()
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            userprofile.save()
            messages.success(request, _('Changes are done.'))
            return HttpResponseRedirect(reverse('homepage'))
        else:
            messages.error(request, _('Edit is failed.'))
    else:
        form = UserProfileForm()
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def postAdd(request):
    if request.method == 'POST':
        form = PostAddForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, _('Post Added !'))
            return HttpResponseRedirect(reverse('homepage'))
        else:
            messages.error(request, _('Post was not Added !'))
    else:
        form = PostAddForm()
    return render(request, 'blogArticles/postadd.html', {'form': form})


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
            messages.success(request,
                             _('Email is changed. Verification mail sent.'))
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, _('Process failed. Try again.'))
            return HttpResponseRedirect(reverse('changeemail'))
    else:
            messages.error(request, _('Process failed. Try again.'))
            form = EmailChangeForm()
    return render(request, 'accounts/emailchange.html', {'form': form})


@login_required
def passwordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = request.user.get_profile()
            user.password = form.save()
            user.save()
            messages.success(request,
                             _('Password has changed.Verification mail sent.'))
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, _('Process failed. Try again.'))
            return HttpResponseRedirect(reverse('changepassword'))
    else:
        messages.error(request, _('Process failed. Try again.'))
        form = PasswordChangeForm()
    return render(request, 'accounts/passwordchange.html', {'form': form})


# @login_required
# def disableAccount(request):
#     if request.method == 'POST':
#         form = AccountDisableForm(request.POST)
#         if form.is_valid():
#             user = User.objects.get(request.user)
#             user.is_active = False
#             user.is_verified = False
#             user.save()
#             messages.success(request, _('Account disabled. Good Bye.'))
#             return HttpResponseRedirect(reverse('index'))
#         else:
#             messages.error(request, _('Process Failed, Try Again.'))
#             form = AccountDisableForm()
#     return render(request, 'accounts/accountdisable.html', {'form': form})
