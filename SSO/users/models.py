from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser, Group
from django.utils.translation import gettext_lazy as _
from gdstorage.storage import GoogleDriveStorage

gd_storage = GoogleDriveStorage()

class Photo(models.Model):
    filename = models.CharField(max_length=255, primary_key=True)
    filetype = models.CharField(max_length=10, blank=True)
    filesize = models.PositiveIntegerField(blank=True, null=True)
    filedata = models.FileField(upload_to='imageProfile/', storage=gd_storage)
    
    def __str__(self):
        return str(self.filename)


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password = None, group='Customer', **kwargs):
        if not email:
            raise ValueError('accounts must have an email address')
        email = self.normalize_email(email)
        email = email.lower()
        
        
        user = self.model(email=email, **kwargs)

        user.set_password(password)
        user.save(using=self._db, group=group)

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
    groups = models.ManyToManyField(Group, related_name='user_accounts', blank=False)
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE, max_length=255,blank=True, null=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def get_full_name(self):
        return self.first_name + self.last_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email
    
    def save(self, group='Customer', *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.groups.exists():
            new_group = Group.objects.get(name=group)
            self.groups.add(new_group)




