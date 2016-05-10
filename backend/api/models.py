from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class OptUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password, )
        user.is_admin = True
        user.is_technician = True
        user.save(using=self._db)
        return user


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name='Company\'s name', help_text='e.g. Coaxis SAS, Akema')


class OptUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE, related_name='employees')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_technician = models.BooleanField(default=False)

    objects = OptUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name_plural = "Users"


class DateMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='created')
    modified = models.DateTimeField(auto_now=True, verbose_name='modified')

    class Meta:
        abstract = True


class RemoteNode(DateMixin):
    """A remote node i.e. OPT-box"""
    name = models.CharField(max_length=255, verbose_name='node\'s name', help_text='Headquarter office or a branch')
    address = models.GenericIPAddressField(help_text='node IPv4 or IPv6 address')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='printers')
