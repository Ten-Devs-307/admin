from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    '''Managers user / voter accounts'''

    def create_user(self, email, password, **kwargs):
        user = self.model(email=email, password=password, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email,  password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
