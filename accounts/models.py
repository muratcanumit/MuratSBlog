from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

GENDER_CHOICES = (
    ('M', _('MALE')),
    ('F', _('FEMALE')),
    ('O', _('OTHER')),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    birth_date = models.DateField(blank=True, verbose_name="Date of Birth")
    gender = models.CharField(max_length=6,
                              choices=GENDER_CHOICES, verbose_name="Gender")
    is_verified = models.BooleanField(default=False)
    # activation key
    act_key = models.CharField(max_length=25)
    # key's expiration
    exp_key = models.DateTimeField()

    def __unicode__(self):
        return u"%s" % self.user.email
