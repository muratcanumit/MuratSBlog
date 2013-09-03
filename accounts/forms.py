from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.db import models
from MuratSBlog.accounts.models import UserProfile
from django import forms
from django.forms import ModelForm
from django.forms import widgets


# Login form for registered users
class LoginForm(forms.Form):
    email = forms.EmailField(required=True,
                             label='EMail',
                             error_messages={
                                 'required': "Enter a correct E-mail Address"})

    password = forms.CharField(widget=forms.PasswordInput,
                               required=True,
                               min_length=6, max_length=11,
                               label='Password',
                               error_messages={
                                   'required': "Enter correct Password"})


# Registration form for unregistered users
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             label='Email',
                             error_messages={
                                 'required': "Email field must be filled"})

    password = forms.CharField(widget=forms.PasswordInput,
                               required=True,
                               min_length=6, max_length=11,
                               label='Password',
                               help_text='Password must be 6 to 11 characters')

    # Re-Typing the password
    password_rt = forms.CharField(widget=forms.PasswordInput,
                                  required=True,
                                  min_length=6, max_length=11,
                                  label='Retype Password',
                                  help_text='Rewrite Your Password')

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'email',
                  'password', 'password_rt')

    def clean_username(self):
        username = self.cleaned_data.['username']
        existing_username = User.objects.get(username=username)
        if existing_username:
            raise forms.ValidationError("This Username is taken before.")

        return self.cleaned_data['username']

    def clean_email(self):
        if UserProfile.is_email_exists(self.cleaned_data['email']):
            raise forms.ValidationError("Typed an invalid email,"
                                        "email might be taken by another"
                                        "user.")

        return self.cleaned_data['email']

    def clean_password(self):
        password = self.cleaned_data.['password']
        password_rt = self.cleaned_data.['password_rt']

        if password != password_rt:
            raise forms.ValidationError("Did not typed password fields same")

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
        username = self.cleaned_data.['username']
        existing_username = User.objects.get(username=username)
        if existing_username:
            raise forms.ValidationError("This Username is taken before.")

        return self.cleaned_data['username']


# User can change email address, have to type password twice and
# confirm the key which is sent by mail
class EmailChangeForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label='new-email'
        help_text='Apply the change with activation key.')

    password = forms.CharField(widget=forms.PasswordInput,
                               required=True,
                               min_length=6, max_length=11,
                               label='Password',
                               help_text='Must be 6 to 11 characters')

    password_check = forms.CharField(widget=forms.PasswordInput,
                                     required=True,
                                     min_length=6, max_length=11,
                                     label='Retype-Password',
                                     help_text='Must be 6 to 11 characters')

    def clean_email(self):
        if UserProfile.is_email_exists(self.cleaned_data['email']):
            raise forms.ValidationError("You typed an invalid email.")

        return self.cleaned_data['email']

    def clean_password(self):
        # c_password is the users current password
        c_password = UserProfile.objects.get(password=password)
        c_password = self.cleaned_data.['c_password']
        password = self.cleaned_data.['password']
        password_check = self.cleaned_data.['password_check']

        if c_password != password or password != password_check:
            raise forms.ValidationError("Typed password fields incorrect")
        
        return self.cleaned_data['c_password']


# User can change Password, have to type actual password once and new one
# twice, also have to confirm the key which is sent by mail
class PasswordChangeForm(PasswordChangeForm):
    # o_password is the user's old password
    o_password = forms.CharField(widget=forms.PasswordInput,
                                 required=True,
                                 min_length=6, max_length=11,
                                 label='old-Password',
                                 help_text='Password must be 6 to 11 Chars',
                                 verbose_name="old password")

    new_password = forms.CharField(widget=forms.PasswordInput,
                                   required=True,
                                   min_length=6, max_length=11,
                                   label='New-Password',
                                   help_text='Rewrite Your Password',
                                   verbose_name="password")

    password_check = forms.CharField(widget=forms.PasswordInput,
                                     required=True,
                                     min_length=6, max_length=11,
                                     label='Retype-New-Password',
                                     help_text='Password Again',
                                     verbose_name="password again")

    def clean_password(self):
        # current password => c_password
        c_password = UserProfile.objects.get(password=password)
        c_password = self.cleaned_data.['c_password']
        new_password = self.cleaned_data.['new_password']
        password_check = self.cleaned_data.['password_check']

        if c_password = new_password or new_password != password_check:
            raise forms.ValidationError("Typed your same password for new one")

        return self.cleaned_data['c_password']


class AccountDisableForm(EmailChangeForm):

    class Meta(EmailChangeForm.Meta):
        model = User
        fields = ('email', 'password', 'password_check')

   
    def save(self, user):
        user.is_active = False
        user.save()
        mail_title = 'Disabling your MuratSBlog account'
        mail_text = ('Hello! You wanted to disable your account. '
                     'We disabled your account and this is very unhappy.\n'
                     'Good Days from MuratSBlog.')

        send_mail(mail_title,
                  mail_text,
                  'muratsdjangoblog@gmail.com',
                  [user.email])
