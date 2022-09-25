import pytest

from django.conf import settings

from pytest_django.fixtures import django_user_model

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(django_user_model):
    # create user
    user = django_user_model.objects.create_user(
        username="dummy1@dispostable.com",
        password="testuser",
    )
    assert user.get_absolute_url() == f"/users/{user.username}/"
