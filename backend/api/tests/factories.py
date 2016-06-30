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
    is_staff = False


class EmployeeFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Employee

    user = factory.SubFactory(UserFactory)
    is_technician = False

    @factory.post_generation
    def company_set(self, create, extracted, **kwargs):
        if not create:  # Simple build, do nothing.
            return

        if extracted:  # A list of objects were passed in, use them
            for company in extracted:
                self.company_set.add(company)


class TechnicianFactory(EmployeeFactory):
    # class Meta:
    #     model = models.Employee
    #
    # user = factory.SubFactory(UserFactory)
    is_technician = True
    #
    # @factory.post_generation
    # def company_set(self, create, extracted, **kwargs):
    #     if not create:  # Simple build, do nothing.
    #         return
    #
    #     if extracted:  # A list of objects were passed in, use them
    #         for company in extracted:
    #             self.company_set.add(company)

class RemoteNodeFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.RemoteNode

    name = 'open-space'
    address = '10.0.254.1'
    company = factory.SubFactory(CompanyFactory)
