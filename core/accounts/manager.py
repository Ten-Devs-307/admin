from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    '''Managers user / voter accounts'''

    def create_user(self, email, name, password, **kwargs):
        user = self.model(email=email, name=name, password=password, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password, **kwargs):
        user = self.create_user(email, name,  password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
