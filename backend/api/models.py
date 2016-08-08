import uuid

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models
from django.db.models.signals import post_save

from api import container_services


class MyUserManager(BaseUserManager):
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
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    first_name = models.CharField(verbose_name='first name', max_length=30, blank=True)
    last_name = models.CharField(verbose_name='last name', max_length=30, blank=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

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


class Employee(DateMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    is_technician = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


def create_employee(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        Employee.objects.create(user=user)


post_save.connect(create_employee, sender=MyUser)


class Company(DateMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    employees = models.ManyToManyField(Employee, blank=True, related_name='companies')

    def __str__(self):
        return self.name


class RemoteNode(DateMixin):
    """A remote node i.e. OPT-box"""
    name = models.CharField(max_length=255, verbose_name='node\'s name', help_text='Headquarter office or a branch')
    address = models.GenericIPAddressField(help_text='node IPv4 or IPv6 address')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='printers')


class MastContainer(DateMixin):
    """MAST (Multi Auto-SSH Tunnel daemon docker"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(blank=True, verbose_name='site location', help_text='Headquarter office or a branch')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='mast_containers')
    container_id = models.TextField(verbose_name='container system config',
                                    help_text='Detailled information about container')

    # def infos(self):
    #     import docker
    #     docker_api = docker.Client(base_url='unix://var/run/docker.sock')
    #     container_data = docker_api.inspect_container(self.container_id)
    #
    #     return container_services.get_container_dict(container_data)
