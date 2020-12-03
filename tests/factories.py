import factory
from factory.django import DjangoModelFactory

from django.contrib.auth import get_user_model

from thebrushstash.models import Country


class CountryFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: 'name%s' % n)

    class Meta:
        model = Country


class UserFactory(DjangoModelFactory):
    first_name = factory.Sequence(lambda n: 'first_name%s' % n)
    last_name = factory.Sequence(lambda n: 'last_name%s' % n)
    username = factory.Sequence(lambda n: 'username%s' % n)
    email = factory.LazyAttribute(lambda o: '%s@example.com' % o.first_name)
    country = factory.SubFactory(CountryFactory)

    class Meta:
        model = get_user_model()


class AdminUserFactory(UserFactory):
    is_staff = True
    is_superuser = True
