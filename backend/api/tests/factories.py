import factory

from api import models


class CompanyFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Company

    name = 'Coaxis'


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.MyUser

    email = factory.Sequence(lambda n: 'u{0}@coaxis.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')
    company = factory.SubFactory(CompanyFactory)
    is_staff = False


class TechnicianFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.MyUser

    email = factory.Sequence(lambda n: 'u{0}@coaxis.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')
    company = factory.SubFactory(CompanyFactory)
    is_technician = True

class RemoteNodeFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.RemoteNode

    name = 'open-space'
    address = '10.0.254.1'
    company = factory.SubFactory(CompanyFactory)
