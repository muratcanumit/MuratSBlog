from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
#, get_object_or_404
# from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext as _

from blogArticles.models import Post
#, Comment
# from accounts.models import UserProfile
from accounts.forms import (LoginForm, RegisterForm,
                            UserProfileForm, EmailChangeForm,
                            PasswordChangeForm)
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
                                   _('Verify account with activation key.'))
                elif user.is_active():
                    user = User.objects.get(user=user)
                    login(request, user)
                    request.session['user'] = dict(
                        id=user.id,
                        is_verified=user.is_verified)
                    messages.success(request, _('Logged in Successful.'))
                    return HttpResponseRedirect(reverse('homepage'))
                else:
                    messages.error(request,
                                   _('Login Failed. Account is inactive.'))
                    return HttpResponseRedirect(reverse('login'))
            else:
                messages.error(
                    request,
                    _('Login Failed. Wrong Username or Password. Try Again.')
                )
                return HttpResponseRedirect(reverse('login'))
    else:
        form = LoginForm
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logoutPage(request):
    logout(request)
    return HttpResponseRedirect('index')


def registerPage(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.create_user(user)
            user.is_active = False
            user.save()
            messages.success(request, _('Successfully Registered.'))
        else:
            messages.error(request, _('Fields have to be correctly filled.'))
            return HttpResponseRedirect(reverse('register'))
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


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
            messages.success(request, _('Your Avatar has changed.'))
            user.save()
            messages.success(request, _('Changes are done.'))
        else:
            messages.error(request, _('Something is wrong.'))
            return HttpResponseRedirect(reverse('editprofile'))
    else:
        form = UserProfileForm()
    return render(request, 'accounts/editprofile.html', {'form': form})


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
