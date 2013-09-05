from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from django.forms import extras
from accounts.models import UserProfile, GENDER_CHOICES
from django.forms import widgets
from django.utils.translation import ugettext as _
#from django.contrib import messages


# Login form for registered users
class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label='EMail',
        error_messages={
            'required': _("Enter a correct E-mail Address")})

    password = forms.CharField(widget=forms.PasswordInput,
                               required=True,
                               label='Password',
                               error_messages={
                                   'required': _("Enter correct Password")})


# Registration form for unregistered users
class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'password1', 'password2')
        exclude = ('first_name', 'last_name')

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #        raise forms.ValidationError(_("This Username is taken before."))
    #     if existing_username:
    #         raise forms.ValidationError(_("This Username is taken before."))

    #     return self.cleaned_data['username']

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     existing_email = User.objects.get(email=email)
    #     if email == existing_email:
    #         raise forms.ValidationError(_("Typed an invalid email,"
    #                                     "email might be taken by another"
    #                                     "user."))

    #     return self.cleaned_data['email']

    def clean_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise forms.ValidationError(_("Typed an invalid email,"
                                        "email might be taken by another"
                                        "user."))

        return self.cleaned_data['email']


# Profile Informations and extras for registered users
class UserProfileForm(forms.ModelForm):
    username = forms.CharField(required=False, label='User name')
    first_name = forms.CharField(required=False, label='First Name')
    last_name = forms.CharField(required=False, label='Last Name')

    class Meta:
        model = UserProfile
        fields = ('username', 'first_name', 'last_name',
                  'user_avatar', 'birth_date', 'gender')
        widgets = {
            'gender': widgets.Select(choices=GENDER_CHOICES),
            'birth_date': extras.SelectDateWidget(years=range(1940, 2013))
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
            raise forms.ValidationError(_("This Username is taken before."))
        except User.DoesNotExist:
            return username


# User can change email address, have to type password twice and
# confirm the key which is sent by mail
class EmailChangeForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label='new-email',
        help_text=_('Enter the new email address.'
                    ' Then, Apply the change with activation key.'))

    password = forms.CharField(widget=forms.PasswordInput,
                               required=True,
                               label='Password',
                               help_text=_('Enter your password'))

    password_check = forms.CharField(widget=forms.PasswordInput,
                                     required=True,
                                     label='Retype-Password',
                                     help_text=_('Enter your password again'))

    def clean_email(self):
        if UserProfile.is_email_exists(self.cleaned_data['email']):
            raise forms.ValidationError(_("You typed an invalid email."))

        return self.cleaned_data['email']

    # def clean_password(self):
    #     # c_password is the users current password
    #     c_password = UserProfile.objects.get(password=password)
    #     c_password = self.cleaned_data['c_password']
    #     password = self.cleaned_data['password']
    #     password_check = self.cleaned_data['password_check']

    #     if c_password != password or password != password_check:
    #         raise forms.ValidationError(_("Typed password fields incorrect"))

    #     return self.cleaned_data['c_password']


# User can change Password, have to type actual password once and new one
# twice, also have to confirm the key which is sent by mail
class PasswordChangeForm(forms.Form):
    # o_password is the user's old password
    c_password = forms.CharField(widget=forms.PasswordInput,
                                 required=True,
                                 label='old-Password',
                                 help_text=_('Enter old-Password'))

    c_password_check = forms.CharField(widget=forms.PasswordInput,
                                       required=True,
                                       label='Retype old-Password',
                                       help_text=_('Again Enter old-Password'))

    new_password = forms.CharField(widget=forms.PasswordInput,
                                   required=True,
                                   label='New-Password',
                                   help_text=_('Rewrite Your Password'))

    password_check = forms.CharField(widget=forms.PasswordInput,
                                     required=True,
                                     label='Retype-New-Password',
                                     help_text=_('New Password Again'))

    # def clean_password(self):
    #     # current password => c_password
    #     c_password = UserProfile.objects.get(
    #         password=self.cleaned_data['c_password'])
    #     # c_password = self.cleaned_data['c_password']
    #     c_password_check = self.cleaned_data['c_password_check']
    #     new_password = self.cleaned_data['new_password']
    #     password_check = self.cleaned_data['password_check']

    #     if c_password != c_password_check:
    #         raise forms.ValidationError(_("Typed passwords Wrong."))
    #     elif c_password == new_password or new_password != password_check:
    #         raise forms.ValidationError(_("Typed same password for new one"))

    #     return self.cleaned_data['c_password']


# class AccountDisableForm(forms.Form):
