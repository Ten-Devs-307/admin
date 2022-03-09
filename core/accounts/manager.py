from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    '''Managers user / voter accounts'''

    def create_customer(self, email, name, password, **kwargs):
        user = self.model(email, name, password, **kwargs)
        user.set_password(password)
        user.is_customer = True
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user

    def create_labourer(self, email, name, password, **kwargs):
        user = self.model(email, name, password, **kwargs)
        user.set_password(password)
        user.is_labourer = True
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user

    def create_superuser(self, email, name, password, **kwargs):
        user = self.model(email, name,  password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
