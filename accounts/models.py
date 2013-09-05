from django.db import models
from django.contrib.auth.models import User


GENDER_CHOICES = (
    ('M', 'MALE'),
    ('F', 'FEMALE'),
    ('O', 'OTHER'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    user_avatar = models.ImageField(upload_to='profile_pics',
                                    verbose_name="User Avatar")
    birth_date = models.DateField(blank=True, verbose_name="Date of Birth")
    gender = models.CharField(max_length=6,
                              choices=GENDER_CHOICES, verbose_name="Gender")
    is_verified = models.BooleanField(default=False)
    # activation key
    act_key = models.CharField(max_length=25)
    # key's expiration
    exp_key = models.DateTimeField()

    def __unicode__(self):
        return u"%s" % self.user.username
