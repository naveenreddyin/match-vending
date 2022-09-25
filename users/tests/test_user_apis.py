import pytest

from users.models import Profile

pytestmark = pytest.mark.django_db


def test_if_login_exists(api_client):
    response = api_client.post("/rest-auth/login/")

    # should give 400 as login creds not passed
    assert response.status_code == 400


def test_if_login_succeeds(
    api_client,
    django_user_model,
):
    # create user
    django_user_model.objects.create_user(
        username="dummy1@dispostable.com",
        password="testuser1234_",
    )
    # call login endpoint
    response = api_client.post(
        "/rest-auth/login/",
        {
            "username": "dummy1@dispostable.com",
            "password": "testuser1234_",
        },
        format="json",
    )

    # should give 200 as login creds are passed
    assert response.status_code == 200


def test_with_wrong_login_creds(
    api_client,
    django_user_model,
):
    # create user
    django_user_model.objects.create_user(
        username="dummy1@dispostable.com",
        password="testuser1234_",
    )
    # call login endpoint
    response = api_client.post(
        "/rest-auth/login/",
        {
            "username": "dummy1@dispostable.com",
            "password": "testuser1234_!",
        },
        format="json",
    )

    # should give 200 as login creds are passed
    assert response.status_code == 400


# registration endpoints
def test_if_registration_url_exists(api_client):
    response = api_client.post("/rest-auth/registration/")
    # should give 400 as login creds not passed
    assert response.status_code == 400


def test_registration_with_proper_data(api_client):
    response = api_client.post(
        "/rest-auth/registration/",
        {
            "username": "dummy2@dispostable.com",
            "password": "testuser1234_",
        },
    )
    # should give 201 as login creds are passed
    assert response.status_code == 201


def test_to_see_if_profile_defaults_set_when_data_not_sent(
    api_client, django_user_model
):
    username = "dummy2@dispostable.com"
    response = api_client.post(
        "/rest-auth/registration/",
        {
            "username": username,
            "password": "testuser1234_",
        },
    )
    # should give 201 as login creds are passed but profile should be also created
    # with defaults
    assert response.status_code == 201
    profile = Profile.objects.get(
        user=django_user_model.objects.get(username=username),
    )
    assert profile.id != 0
    # assert that is_buyer and is_seller is set to false and deposit is zero
    assert profile.is_buyer == False
    assert profile.is_seller == False
    assert profile.deposit == 0


def test_when_profile_fields_are_set(api_client, django_user_model):
    username = "dummy2@dispostable.com"
    response = api_client.post(
        "/rest-auth/registration/",
        {
            "username": username,
            "password": "testuser1234_",
            "is_buyer": True,
            "deposit": 100,
        },
        format="json",
    )
    # should give 201 as login creds are passed but profile is set with non default values
    assert response.status_code == 201
    profile = Profile.objects.get(
        user=django_user_model.objects.get(username=username),
    )
    assert profile.id != 0
    # assert that is_buyer is set to true and deposit is 100
    assert profile.is_buyer == True
    assert profile.deposit == 100


def test_deposit_validation(api_client):
    username = "dummy2@dispostable.com"
    response = api_client.post(
        "/rest-auth/registration/",
        {
            "username": username,
            "password": "testuser1234_",
            "deposit": 101,
        },
        format="json",
    )
    # should give 400 as deposit value is not a multiple of 5
    assert response.status_code == 400
    assert response.data == {"deposit": ["deposit is not multiple of 5"]}
