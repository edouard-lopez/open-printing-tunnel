import factory

from api import models


class ClientFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Client

    name = 'Coaxis'


@factory.django.mute_signals(models.post_save)
class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.MyUser

    email = factory.Sequence(lambda n: 'u{0}@coaxis.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')
    is_staff = False


class EmployeeFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Employee

    user = factory.SubFactory(UserFactory)
    is_technician = False

    @factory.post_generation
    def clients(self, create, extracted, **kwargs):
        if not create:  # Simple build, do nothing.
            return

        if extracted:  # A list of objects were passed in, use them
            for client in extracted:
                self.clients.add(client)


class TechnicianFactory(EmployeeFactory):
    is_technician = True


class DaemonFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Daemon

    client = factory.SubFactory(ClientFactory)
