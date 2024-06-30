from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.utils.translation import gettext_lazy as _

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password = None, **kwargs):
        if not email:
            raise ValueError('accounts must have an email address')
        email = self.normalize_email(email)
        email = email.lower()
        
        
        user = self.model(email=email, **kwargs)

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password = None, **kwargs):
        user = self.create_user(
            email,
            password=password,
            **kwargs
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    data_iscrizione = models.DateField(_('data iscrizione'), auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def get_full_name(self):
        return self.first_name + self.last_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email