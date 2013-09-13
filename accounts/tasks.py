from celery.task import task
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from accounts.models import UserProfile
import datetime
import pytz
from random import random
from django.utils.hashcompat import sha_constructor
from MuratSBlog.settings import KEY_EXPIRES_DATE


def mail_send(act_key, cause, user_email, subject):
    verify_url = generate_url(act_key, cause)
    message_body = _('Activation URL: ') + str(verify_url)
    send_mail(subject, message_body,
              'muratsdjangoblog@gmail.com',
              [user_email])


def generate_url(act_key, cause="activation"):
    if cause == "activation":
        verify_url = Site.objects.get_current() + "account/act/"+str(
            act_key)
    return verify_url


def generate_key_expires_date():

    exp_key = datetime.datetime.today() + datetime.timedelta(
        KEY_EXPIRES_DATE
    )
    return exp_key


def is_key_expires(key_expires_date):
    if key_expires_date <= datetime.datetime.utcnow().replace(
            tzinfo=pytz.utc):
        return True
    else:
        return False


def send_activation_code(act_key, user_email, cause="activation"):

    if cause == "activation":
        send_mail(act_key, cause, ['user_email'], _('Activation Code'))


def generate_activation_key(user):
    salt = sha_constructor(str(random()) + user).hexdigest()[:20]
    return salt
