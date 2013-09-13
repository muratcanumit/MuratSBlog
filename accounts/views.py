import datetime
from random import choice
from string import letters
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext as _
from accounts.models import UserProfile
from accounts.forms import (LoginForm, RegisterForm,
                            UserProfileForm, EmailChangeForm,
                            ChangePasswordForm, AccountDisableForm)
from accounts import tasks


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
                if user.is_active is False and user.userprofile.is_verified is False:
                    messages.error(request,
                                   _('Verify account with activation key.'))
                    return redirect(reverse('login'))
                elif user.is_active is True and user.userprofile.is_verified is True:
                    login(request, user)
                    return redirect(reverse('index'))

            else:
                messages.error(
                    request,
                    _('Invalid Email or Password. If new '
                      'Registered Verify your account with the email.')
                )
                return redirect(reverse('login'))
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required(login_url='/login/')
def logoutPage(request):
    logout(request)
    return redirect('/')


def registerPage(request):

    if request.method == 'POST':
        data = request.POST.copy()
        form = RegisterForm(data)

        if form.is_valid():
            data['username'] = ''.join([choice(letters) for i in xrange(30)])
            # data['password'] = ''.join([choice(letters) for i in xrange(30)])
            if form.cleaned_data['password'] != form.cleaned_data['password2']:
                messages.error(request, _('Passwords are not matched.'))
                form = RegisterForm()
            else:

                act_key = tasks.generate_activation_key(data['email'])
                exp_key = tasks.generate_key_expires_date()
                # tasks.send_activation_code(act_key, data['email'])

                user = form.save()
                user.set_password(form.cleaned_data['password'])
                user.username = data['username']
                user.email = form.cleaned_data['email']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.is_active = False
                user.save()
                try:
                    userprofile = user.userprofile
                except UserProfile.DoesNotExist:
                    userprofile = form.instance

                userprofile.user = user
                userprofile.is_verified = False
                userprofile.act_key = act_key
                userprofile.exp_key = exp_key
                userprofile.save()
                messages.success(request, _('Registered!'))
                return redirect(reverse('login'))
        else:
            messages.error(request, _('Please Fill Fields Correctly.'))
            form = RegisterForm()
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required(login_url='/login/')
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
            userprofile.gender = form.cleaned_data['gender']
            userprofile.birth_date = form.cleaned_data['birth_date']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            userprofile.save()
            messages.success(request, _('Changes are done.'))
            return redirect(reverse('profile'))
        else:
            messages.error(request, _('Edit is failed.'))
            return redirect(reverse('register'))
    else:
        form = UserProfileForm()

    return render(request, 'accounts/profile.html', {'form': form})


@login_required(login_url='/login/')
def change_email(request):
    user = request.user
    data = request.POST.copy()
    if request.method == 'POST':
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            if user.check_password(form.cleaned_data['password']) is False:
                messages.error(request, _('Password is wrong.'))
                form = ChangePasswordForm()
            else:
                user.email = form.cleaned_data['email']
                user.is_active = False
                user.save()

                act_key = tasks.generate_activation_key(data['email'])
                exp_key = tasks.generate_key_expires_date()
                # tasks.send_activation_code(act_key, data['email'])

                try:
                    userprofile = user.userprofile
                except UserProfile.DoesNotExist:
                    userprofile = form.instance

                userprofile.user = user
                userprofile.is_verified = False
                userprofile.act_key = act_key
                userprofile.exp_key = exp_key
                userprofile.save()

                messages.success(request,
                                 _('Email is changed. Verification mail sent.'))
            return redirect(reverse('index'))
        else:
            messages.error(request, _('Change failed. Enter your Password Correct.'))
            return redirect(reverse('changeemail'))
    else:
        form = EmailChangeForm()
    return render(request, 'accounts/email_change.html', {'form': form})


@login_required(login_url='/login/')
def change_password(request):
    user = request.user
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if user.check_password(form.cleaned_data['old_password']) is False:
                messages.error(request, _('Password is wrong.'))
                form = ChangePasswordForm()
            elif form.cleaned_data['new_password1'] != form.cleaned_data['new_password2']:
                messages.error(request, _('Passwords are not matched.'))
                form = ChangePasswordForm()
            else:
                user.set_password(form.cleaned_data['new_password1'])
                user.save()
                messages.success(request, _('Password changed'))
            return redirect(reverse('profile'))
        else:
            messages.error(request, _('Change is failed.'))
            return redirect(reverse('changepassword'))
    else:
        form = ChangePasswordForm()
    return render(request, 'accounts/change_password.html', {'form': form})


@login_required(login_url='/login/')
def disable_account(request):
    user = request.user
    if request.method == "POST":
        form = AccountDisableForm(request.POST)
        if form.is_valid():
            if user.check_password(form.cleaned_data['password1']) is False:
                messages.error(request, _('Password is wrong.'))
                form = AccountDisableForm()
            elif form.cleaned_data['password1'] != form.cleaned_data['password2']:
                messages.error(request, _('Passwords are not matched.'))
                form = AccountDisableForm()
            else:
                user = User.objects.get(request.user)
                user.is_active = False
                user.save()
                messages.success(request, _('Account disabled. Good Bye.'))
            return redirect(reverse('index'))
        else:
            messages.error(request, _('You Typed Wrong Passwords, Try Again.'))
            return redirect(reverse('disableaccount'))
    else:
        form = AccountDisableForm()
    return render(request, 'accounts/disable_account.html', {'form': form})


def verify_user(request, act_key):

    userprofile = get_object_or_404(UserProfile, act_key=act_key)
    if not userprofile.is_verified:
        if not tasks.is_key_expires(userprofile.exp_key):
            dic = {"message": _('Account is activated')}
            userprofile.user.is_active = True
            userprofile.is_verified = True
            userprofile.save()
            userprofile.user.save()
        else:
            dic = {"message": _('Activation key is expired')}
    else:
        dic = {"message": _('You Are Active.')}
    return render(request, 'accounts/activate_user.html', dic)


def terms_of_use(request):
    return render(request, 'accounts/terms_of_use.html')


def social(request):
    return render(request, 'accounts/social.html')


def authors(request):
    authors = User.objects.filter(is_active=True).order_by('date_joined')
    return render(request, 'accounts/authors.html',
                  {'authors': authors})
