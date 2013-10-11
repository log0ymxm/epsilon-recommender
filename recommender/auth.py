from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from tastypie.models import create_api_key
from django.utils.encoding import python_2_unicode_compatible

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=CustomUserManager.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email,
            password=password,
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

@python_2_unicode_compatible
class CustomUser(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(unique=True, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    verified = models.BooleanField(default=False, help_text='Has the user verified his email address yet?')
    bio = models.CharField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=255, help_text='User preferred name')
    url = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = 'user'

    def get_full_name(self):
        return self.name or self.email

    def get_short_name(self):
        return self.name or self.email

    @property
    def is_staff(self):
        return self.is_admin

    def __unicode__(self):
        return self.get_short_name()

models.signals.post_save.connect(create_api_key, sender=CustomUser)
