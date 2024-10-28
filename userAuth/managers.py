from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):

    def _create_user(self, email,is_staff,is_superuser, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user  = self.model(email=email, is_staff = is_staff, is_superuser = is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self,email,password,**extra_fields):
        return self._create_user(email,False,False,password,**extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, True, True, password,**extra_fields)