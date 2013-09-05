from django.conf.urls import patterns, url
# from django.contrib.auth.models import User
# from accounts.models import UserProfile

urlpatterns = patterns(
    'accounts.views',
    url(r'^login/$', 'loginPage', name="login"),
    url(r'^logout/$', 'logoutPage', name="logout"),
    url(r'^register/$', 'registerPage', name="register"),
    url(r'^account/profile/$', 'editProfile', name="profile"),
    url(r'^account/change-email/$', 'emailChange', name="changeemail"),
    url(
        r'^account/change-password/$', 'passwordChange', name="changepassword"
    ),
    url(r'^homepage/$', 'homepage', name="homepage"),
    url(r'^homepage/postadd/$', 'postAdd', name="postadd"),
    url(r'^homepage/posts/(?P<post_id>\d+)/detailed/$',
        'detailed', name="detailed"),
)
