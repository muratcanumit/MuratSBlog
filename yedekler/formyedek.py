from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from MuratSBlog.accounts.models import UserProfile
from django import forms
from django.forms import ModelForm
from django.core.mail import send_mail


# Login form for registered users
class LoginForm(forms.Form):
    email = forms.EmailField(required=True,
                             verbose_name="Email",
                             label='EMail',
                             error_messages={
                                 'required': "Enter a correct E-mail Address"})

    password = forms.CharField(widget=forms.PasswordInput,
                               verbose_name="Password",
                               required=True,
                               min_length=6, max_length=11,
                               label='Password',
                               error_messages={
                                   'required': "Enter correct Password"})


# Registration form for unregistered users
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             verbose_name="Email",
                             label='E-mail',
                             error_messages={
                                 'required': "E-mail field must be filled"})

    password = forms.CharField(widget=forms.PasswordInput,
                               required=True,
                               verbose_name="Password",
                               min_length=6, max_length=11,
                               label='Password',
                               help_text='Password must be 6 to 11 characters')

    # Re-Typing the password
    password_rt = forms.CharField(widget=forms.PasswordInput,
                                  required=True,
                                  verbose_name="Retype Password",
                                  min_length=6, max_length=11,
                                  label='Retype-Password',
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
            raise forms.ValidationError("You typed an invalid email,"
                                        "email might be taken by another"
                                        "user. Type another email address.")

        return self.cleaned_data['email']

    def clean_password(self):
        password = self.cleaned_data.['password']
        password_rt = self.cleaned_data.['password_rt']

        if password != password_rt:
            raise forms.ValidationError("Did not typed password fields same")

        return self.cleaned_data['password']

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'],
                                        email=self.cleaned_data['email'],
                                        password=self.cleaned_data['password'])

        # User is saved to database but not active, staff or superuser
        # User must verify own account with sent activation key with email
        user.is_superuser = False
        user.is_staff = False
        user.is_active = False
        user.save()

        # Lastly sending an email to the  new registered user
        # contains activation key to verify user's account
        # act_key means activation key, exp_key means
        # expiration condition of activation key
        act_key = utils.create_activation_key(user, user.email)
        exp_key = utils.create_expire_date()
        mail_title = 'Activation of your account for MuratSBlog'
        mail_text = ('Welcome to the MuratSBlog. The last one, you need to'
                     'verify your account with your Activation Key.\n'
                     'Please click the Url and enjoy the Amazing Blog.'
                     'NOTE THAT: Your key is valid for 10 hours\n\n'
                     'Activation Key:\n'
                     'http://localhost:8000/activate/%s') % act_key

        send_mail(mail_title,
                  mail_text,
                  'muratsdjangoblog@gmail.com',
                  [user.email])


# Profile Informations and extras for registered users
class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False, verbose_name="First Name")
    last_name = forms.CharField(required=False, verbose_name="Last Name")

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name',
                  'user_avatar', 'birth_date', 'gender')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = kwargs['instance'].user.first_name
        self.fields['last_name'].initial = kwargs['instance'].user.last_name

    def save(self, commit=True):
        super(UserProfileForm, self).save(self)
        user = self.instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


# User can change email address, have to type password twice and
# confirm the key which is sent by mail
class EmailChangeForm(forms.Form):
    new_email = forms.EmailField(required=True,
                                 verbose_name="change email address",
                                 label='new-email'
                                 help_text='After change your email,\n'
                                 'you need to apply change with the'
                                 'key that sent to your new email address.')

    password_check = forms.CharField(widget=forms.PasswordInput,
                                     required=True,
                                     verbose_name="Password",
                                     min_length=6, max_length=11,
                                     label='Password',
                                     help_text='Must be 6 to 11 characters')

    #pw_check_rt is for checking password by retyping for user security
    pw_check_rt = forms.CharField(widget=forms.PasswordInput,
                                  required=True,
                                  verbose_name="Retype Password",
                                  min_length=6, max_length=11,
                                  label='Password',
                                  help_text='Must be 6 to 11 characters')

    def clean_email(self):
        if UserProfile.is_email_exists(self.cleaned_data['email']):
            raise forms.ValidationError("You typed an invalid email,"
                                        "email might be taken by another"
                                        "user. Type another email address.")

        return self.cleaned_data['email']

    def clean_password(self):
        # c_password is the users current password
        c_password = UserProfile.objects.get(password=password)
        c_password = self.cleaned_data.['c_password']
        password_check = self.cleaned_data.['password_check']
        pw_check_rt = self.cleaned_data.['pw_check_rt']

        if c_password != password_check and password_check != pw_check_rt:
            raise forms.ValidationError("Typed password fields incorrect")

        return self.cleaned_data['c_password']

    def save(self, user):
        # info is the keyword that profile informations from
        # database for User's Profile Fields Values
        info = UserProfile.objects.get(user=user)

        info.act_key = utils.create_activation_key(
            user, self.cleaned_data["new_email"])

        info.exp_key = utils.create_expire_date()
        info.save()

        mail_title = 'Activation of your new E-mail Address for MuratSBlog'
        mail_text = ('Hello! You changed your E-Mail, So you need to'
                     'confirm your change with the key we sent.'
                     'NOTE THAT: Your key is valid for 10 hours\n\n'
                     'Confirmation Key:\n'
                     'http://localhost:8000/confirm/email/%s') % info.act_key

        send_mail(mail_title,
                  mail_text,
                  'muratsdjangoblog@gmail.com',
                  [self.cleaned_data["new_email"]])


# User can change Password, have to type actual password once and new one
# twice, also have to confirm the key which is sent by mail
class PasswordChangeForm(forms.Form):
    # o_password is the user's old password
    o_password = forms.CharField(widget=forms.PasswordInput,
                                 required=True,
                                 verbose_name="Old Password"
                                 min_length=6, max_length=11,
                                 label='Password',
                                 help_text='Password must be 6 to 11 Chars')
    # n_password is the new one of user's password
    n_password = forms.CharField(widget=forms.PasswordInput,
                                 required=True,
                                 verbose_name="New Password"
                                 min_length=6, max_length=11,
                                 label='NewPassword',
                                 help_text='Rewrite Your Password')

    # Re-Typing the new password as n_password
    n_password_rt = forms.CharField(widget=forms.PasswordInput,
                                    required=True,
                                    verbose_name="Retype New Password"
                                    min_length=6, max_length=11,
                                    label='Retype Password',
                                    help_text='Password Again')

    def clean_password(self):
        c_password = UserProfile.objects.get(password=password)
        c_password = self.cleaned_data.['c_password']
        n_password = self.cleaned_data.['password_check']
        n_password_rt = self.cleaned_data.['pw_check_rt']

        if c_password != password_check and password_check and != pw_check_rt:
            raise forms.ValidationError("Did not typed password fields same")

        return self.cleaned_data['c_password']

    def save(self, user):
        # info is the keyword that profile informations from
        # database for User's Profile Fields Values
        info = UserProfile.objects.get(user=user)

        info.act_key = utils.create_activation_key(user, user.email)

        info.exp_key = utils.create_expire_date()
        info.save()

        mail_title = 'Password Change confirmation for MuratSBlog'
        mail_text = ('Hello! You changed your Password, So you need to '
                     'confirm your change with the key we sent. '
                     'NOTE THAT: Your key is valid for 10 hours.\n\n'
                     'Confirmation Key:\n'
                     'http://localhost:8000/confirm/password/%s') % info.act_key

        send_mail(mail_title,
                  mail_text,
                  'muratsdjangoblog@gmail.com',
                  [user.email])


class AccountDisableForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput,
                               required=True,
                               verbose_name="Password"
                               min_length=6, max_length=11,
                               label='Password',
                               help_text='Type Your Password')

    password_rt = forms.CharField(widget=forms.PasswordInput,
                                  required=True,
                                  verbose_name="Retype Password"
                                  min_length=6, max_length=11,
                                  label='Retype Password',
                                  help_text='Rewrite Your Password')

    def clean_password(self):
        c_password = UserProfile.objects.get(password=password)
        c_password = self.cleaned_data.['c_password']
        password = self.cleaned_data.['password']
        password_rt = self.cleaned_data.['password_rt']

        if c_password != password and password != password_rt:
            raise forms.ValidationError("Did not typed password fields same")

        return self.cleaned_data['password']

    def delete_user(self, user):
        user.is_active = False
        mail_title = 'Disabling your MuratSBlog account'
        mail_text = ('Hello! You wanted to disable your account. '
                     'We disabled your account and this is very unhappy.\n'
                     'Good Days from MuratSBlog.')

        send_mail(mail_title,
                  mail_text,
                  'muratsdjangoblog@gmail.com',
                  [user.email])

        user.delete()
