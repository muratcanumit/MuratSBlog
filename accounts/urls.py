from django.conf.urls import patterns, url
# from django.contrib.auth.models import User
# from accounts.models import UserProfile

urlpatterns = patterns(
    'accounts.views',
    url(r'^login/$', 'loginPage', name="login"),
    url(r'^logout/$', 'logoutPage', name="logout"),
    url(r'^register/$', 'registerPage', name="register"),
    url(r'^account/profile/$', 'editProfile', name="profile"),
    url(r'^account/change_email/$', 'change_email', name="changeemail"),
    url(
        r'^account/change_password/$', 'change_password', name="changepassword"
    ),
    url(
        r'^account/disable_account/$', 'disable_account', name="disableaccount"
    ),
    url(r'^terms_of_use/$', 'terms_of_use', name="terms_of_use"),
    url(r'^authors/$', 'authors', name="authors"),
    url(r'^social/$', 'social', name="social"),
)
