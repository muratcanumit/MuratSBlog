from django.conf.urls import patterns, url
from django.contrib.auth.models import User
from accounts.models import UserProfile

urlpatterns = patterns(
    'accounts.views',
    url(r'^$', 'homepage', name="homepage"),
    url(r'^login/$', 'loginPage', name="login"),
    url(r'^register/$', 'registerPage', name="register"),
    url(r'^account/profile-edit/$', 'editProfile', name="editprofile"),
    url(r'^account/change-email/$', 'emailChange', name="changeemail"),
    url(r'^account/change-password/$', 'passwordChange', name="changepassword"),
    # url(r'^disable-account/$', 'disableAccount', name="accountdisable"),
)
