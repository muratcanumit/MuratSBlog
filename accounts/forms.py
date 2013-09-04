from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.db import models
from django import forms

from accounts.models import UserProfile, GENDER_CHOICES
from django.forms import widgets
from django.utils.translation import ugettext as _


# Login form for registered users
class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label='EMail',
        error_messages={
            'required': _("Enter a correct E-mail Address")})

    password = forms.CharField(widget=forms.PasswordInput,
                               required=True,
                               min_length=6, max_length=11,
                               label='Password',
                               error_messages={
                                   'required': _("Enter correct Password")})


# Registration form for unregistered users
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             label='Email',
                             error_messages={
                                 'required': _("Email field must be filled")})

    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        min_length=6, max_length=11,
        label=_('Password'),
        help_text=_('Password must be 6 to 11 characters'))

    # Re-Typing the password
    password_rt = forms.CharField(widget=forms.PasswordInput,
                                  required=True,
                                  min_length=6, max_length=11,
                                  label=_('Retype Password'),
                                  help_text=_('Rewrite Your Password'))

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'email',
                  'password', 'password_rt')

    def clean_username(self):
        username = self.cleaned_data['username']
        existing_username = User.objects.get(username=username)
        if existing_username:
            raise forms.ValidationError(_("This Username is taken before."))

        return self.cleaned_data['username']

    def clean_email(self):
        if UserProfile.is_email_exists(self.cleaned_data['email']):
            raise forms.ValidationError(_("Typed an invalid email,"
                                        "email might be taken by another"
                                        "user."))

        return self.cleaned_data['email']

    def clean_password(self):
        password = self.cleaned_data['password']
        password_rt = self.cleaned_data['password_rt']

        if password != password_rt:
            raise forms.ValidationError(_("Password fields are not same"))

        return self.cleaned_data['password']


# Profile Informations and extras for registered users
class UserProfileForm(forms.ModelForm):
    username = forms.CharField(required=False, label='Username')
    first_name = forms.CharField(required=False, label='First Name')
    last_name = forms.CharField(required=False, label='Last Name')

    class Meta:
        model = UserProfile
        fields = ('username', 'first_name', 'last_name',
                  'user_avatar', 'birth_date', 'gender')
        widgets = {
            'gender': widgets.Select(choices=GENDER_CHOICES)
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        existing_username = User.objects.get(username=username)
        if existing_username:
            raise forms.ValidationError(_("This Username is taken before."))

        return self.cleaned_data['username']


# User can change email address, have to type password twice and
# confirm the key which is sent by mail
class EmailChangeForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label='new-email',
        help_text=_('Apply the change with activation key.'))

    password = forms.CharField(widget=forms.PasswordInput,
                               required=True,
                               min_length=6, max_length=11,
                               label='Password',
                               help_text=_('Must be 6 to 11 characters'))

    password_check = forms.CharField(widget=forms.PasswordInput,
                                     required=True,
                                     min_length=6, max_length=11,
                                     label='Retype-Password',
                                     help_text=_('Must be 6 to 11 characters'))

    def clean_email(self):
        if UserProfile.is_email_exists(self.cleaned_data['email']):
            raise forms.ValidationError(_("You typed an invalid email."))

        return self.cleaned_data['email']

    def clean_password(self):
        # c_password is the users current password
        c_password = UserProfile.objects.get(password=password)
        c_password = self.cleaned_data['c_password']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']

        if c_password != password or password != password_check:
            raise forms.ValidationError(_("Typed password fields incorrect"))

        return self.cleaned_data['c_password']


# User can change Password, have to type actual password once and new one
# twice, also have to confirm the key which is sent by mail
class PasswordChangeForm(PasswordChangeForm):
    # o_password is the user's old password
    o_password = forms.CharField(widget=forms.PasswordInput,
                                 required=True,
                                 min_length=6, max_length=11,
                                 label='old-Password',
                                 help_text=_('Password must be 6 to 11 Chars'),
                                 verbose_name=_("old password"))

    new_password = forms.CharField(widget=forms.PasswordInput,
                                   required=True,
                                   min_length=6, max_length=11,
                                   label='New-Password',
                                   help_text=_('Rewrite Your Password'),
                                   verbose_name=_("password"))

    password_check = forms.CharField(widget=forms.PasswordInput,
                                     required=True,
                                     min_length=6, max_length=11,
                                     label='Retype-New-Password',
                                     help_text=_('Password Again'),
                                     verbose_name=_("password again"))

    def clean_password(self):
        # current password => c_password
        c_password = UserProfile.objects.get(password=password)
        c_password = self.cleaned_data['c_password']
        new_password = self.cleaned_data['new_password']
        password_check = self.cleaned_data['password_check']

        if c_password == new_password or new_password != password_check:
            raise forms.ValidationError(_("Typed same password for new one"))

        return self.cleaned_data['c_password']


class AccountDisableForm(EmailChangeForm):

    class Meta(EmailChangeForm.Meta):
        model = User
        fields = ('email', 'password', 'password_check')
