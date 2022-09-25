import pytest

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from users.tests.factories import UserFactory
from products.models import Product
from products.tests.factories import ProductFactory


@pytest.fixture(autouse=True)
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**kwargs):
        proto_user = UserFactory.build()
        kwargs["password"] = proto_user._password
        if "username" not in kwargs:
            kwargs["username"] = proto_user.username
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.username, password=test_password)
        return client, user

    return make_auto_login


@pytest.fixture
def get_any_user_token_and_client(db, create_user, api_client):

    user = create_user()
    token, _ = Token.objects.get_or_create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return token, api_client


@pytest.fixture
def get_seller_user_token_and_client(db, create_user, api_client):

    user = create_user()
    profile = user.user_profile
    profile.is_seller = True
    profile.save()
    token, _ = Token.objects.get_or_create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return token, api_client


@pytest.fixture
def get_product(db, create_user):
    # process user
    user = create_user()
    profile = user.user_profile
    profile.is_seller = True
    profile.save()
    # create product
    proxy_product = ProductFactory.build()
    product = Product.objects.create(
        name=proxy_product.name,
        amount=10,
        cost=10,
        seller=user,
    )
    return product


@pytest.fixture
def get_product_and_client(db, get_product, api_client):
    product = get_product
    token, _ = Token.objects.get_or_create(user=product.seller)
    api_client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return product, api_client
