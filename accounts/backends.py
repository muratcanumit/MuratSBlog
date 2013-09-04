# This Class provides to backend of site, When User approach to login form
# User should type his email instead of the username. Login Form includes only
# Email and Password fields.
from django.contrib.auth.models import User
from accounts.models import UserProfile


class EmailAuthenticateBackends():
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                try:
                    # User needs to click activation key if user try to logs
                    # in first time sent by email to him for verification
                    # Also if user tries to log in his disabled account
                    # checking is_active from the database is_active field
                    # is_active's value False (0) users can not login to site
                    userprofile = UserProfile.objects.get(user=user)
                    if userprofile.is_verified and user.is_active:
                        return user
                    else:
                        return None
                except UserProfile.DoesNotExist:
                    return user
            else:
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        # Is there a user with that id ? Considers it.
        # If there is, returns user's id, if not returns None Value
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
