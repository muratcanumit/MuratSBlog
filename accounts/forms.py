import datetime
from django.contrib.auth.models import User
from django import forms
from django.forms import extras
from accounts.models import UserProfile, GENDER_CHOICES
from django.forms import widgets
from django.utils.translation import ugettext as _


# Login form for registered users
class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label=_('EMail'),
        error_messages={
            'required': _("Enter a correct E-mail Address")})

    password = forms.CharField(widget=forms.PasswordInput,
                               required=True,
                               label=_('Password'),
                               error_messages={
                                   'required': _("Enter correct Password")})


# Registration form for unregistered users
class RegisterForm(forms.ModelForm):
    username = forms.CharField(required=False, label=_('Username'))

    first_name = forms.CharField(required=False, label=_('First Name'))

    last_name = forms.CharField(required=False, label=_('Last Name'))

    email = forms.EmailField(required=True, label=_('Email'))

    password = forms.CharField(widget=forms.PasswordInput,
                               required=True,
                               label=_('Password'))

    password2 = forms.CharField(widget=forms.PasswordInput,
                                required=True,
                                label=_('Password Again'))

    class Meta:
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'email', 'password', 'password2')

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            email = User.objects.get(email=email)
            raise forms.ValidationError(_('This email is taken before.'))
        except User.DoesNotExist:
            return self.cleaned_data['email']

    # def clean_password(self):
    #     password = self.cleaned_data["password"]
    #     password2 = self.cleaned_data["password2"]
    #     if password != password2:
    #         raise forms.ValidationError(_('Passwords are not matched.'))
    #     else:
    #         return password


# Profile Informations and extras for registered users
class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False, label=_('First Name'))
    last_name = forms.CharField(required=False, label=_('Last Name'))

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name',
                  'birth_date', 'gender')
        widgets = {
            'gender': widgets.Select(choices=GENDER_CHOICES),
            'birth_date': extras.SelectDateWidget(
                years=range(1930, datetime.date.today().year))
        }


#User can change email address, have to type password twice and
#confirm the key which is sent by mail
class EmailChangeForm(forms.Form):
    email = forms.EmailField(required=True, label=_('new email'),
                             help_text=_('Enter the new email address.'
                                         ' Then, Verify with activation key.'))

    password = forms.CharField(widget=forms.PasswordInput,
                               required=True,
                               label=_('Password'))

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            email = User.objects.get(email=email)
            raise forms.ValidationError(_('This email is taken before.'))
        except User.DoesNotExist:
            return self.cleaned_data['email']


# User can change Password, have to type actual password once and new one
# twice, also have to confirm the key which is sent by mail
class ChangePasswordForm(forms.Form):

    old_password = forms.CharField(widget=forms.PasswordInput,
                                   required=True,
                                   label=_('Old Password'))

    new_password1 = forms.CharField(widget=forms.PasswordInput,
                                    required=True,
                                    label=_('New Password'))

    new_password2 = forms.CharField(widget=forms.PasswordInput,
                                    required=True,
                                    label=_('New Password Again'))

    def clean_password(self):
        new_password1 = self.cleaned_data["new_password1"]
        new_password2 = self.cleaned_data["new_password2"]
        if new_password1 != new_password2:
            raise forms.ValidationError(_('Passwords are not matched.'))
        else:
            return new_password1


class AccountDisableForm(forms.Form):

    password1 = forms.CharField(widget=forms.PasswordInput,
                                required=True,
                                label=_('Password'))

    password2 = forms.CharField(widget=forms.PasswordInput,
                                required=True,
                                label=_('Password Again'))

    def clean_password(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_('Passwords are not matched.'))
        else:
            return password1
