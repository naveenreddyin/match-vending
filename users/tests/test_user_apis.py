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
    assert profile.deposit == None


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


def test_user_deposit_endpoint_get_method(api_client):
    response = api_client.get("/users/deposits/")
    # should give 404 as it should only be patch
    assert response.status_code == 404


def test_user_deposit_endpoint_post_method(api_client):
    response = api_client.post("/users/deposits/")
    # should give 404 as it should only be patch
    assert response.status_code == 404


def test_user_deposit_endpoint_put_method(api_client):
    response = api_client.put("/users/deposits/")
    # should give 404 as it should only be patch
    assert response.status_code == 404


def test_user_deposit_endpoint_delete_method(api_client):
    response = api_client.delete("/users/deposits/")
    # should give 404 as it should only be patch
    assert response.status_code == 404


def test_user_deposit_endpoint_patch_method_with_any_role(
    get_any_user_token_and_client,
):
    _, api_client = get_any_user_token_and_client
    response = api_client.patch(
        "/users/deposits/1/",
        {
            "deposit": 10,
        },
        format="json",
    )
    # should give 403 as it should only be is_buyer role
    assert response.status_code == 403


def test_user_deposit_with_buyer_role(get_buyer_user_token_and_client):
    _, api_client = get_buyer_user_token_and_client
    response = api_client.patch(
        "/users/deposits/1/",
        {
            "deposit": 5,
        },
        format="json",
    )
    # should give 200 as it should only be is_buyer role
    assert response.status_code == 200


def test_user_deposit_validation_with_wrong_data(get_buyer_user_token_and_client):
    _, api_client = get_buyer_user_token_and_client
    response = api_client.patch(
        "/users/deposits/1/",
        {
            "deposit": 1,
        },
        format="json",
    )
    # should give 400 as it deposit amount is wrong
    assert response.status_code == 400


def test_user_deposit_validation_with_right_data(
    get_buyer_user_token_and_client, django_user_model
):
    _, api_client = get_buyer_user_token_and_client
    response = api_client.patch(
        "/users/deposits/1/",
        {
            "deposit": 5,
        },
        format="json",
    )
    # should give 200 as it deposit amount is wrong
    assert response.status_code == 200
    # check user
    user = django_user_model.objects.get(pk=1)
    assert user.user_profile.deposit == 5


def test_if_reset_deposit_exists(get_any_user_token_and_client):
    _, api_client = get_any_user_token_and_client

    response = api_client.patch("/users/reset/1/")
    # as user is not authenticated it will give 403
    assert response.status_code == 403


def test_if_reset_deposit_give_404_if_user_not_found(get_buyer_user_product_and_client):
    _, _, api_client = get_buyer_user_product_and_client()

    response = api_client.patch("/users/reset/2/")
    # as user is not authenticated it will give 404
    assert response.status_code == 404


def test_if_reset_deposit_is_success(get_buyer_user_product_and_client):
    user, _, api_client = get_buyer_user_product_and_client(deposit=50)

    assert user.user_profile.deposit == 50

    response = api_client.patch(f"/users/reset/{user.id}/")
    # as user is not authenticated it will give 404
    assert response.status_code == 200

    user.refresh_from_db()
    assert user.user_profile.deposit == 0


def test_multiple_login_not_allowed(api_client, django_user_model):
    # create user
    django_user_model.objects.create_user(
        username="dummy1@dispostable.com",
        password="testuser1234_",
    )
    response = api_client.post(
        "/rest-auth/login/",
        {
            "username": "dummy1@dispostable.com",
            "password": "testuser1234_",
        },
        format="json",
    )
    assert response.status_code == 200
    # try again and should give 403
    response = api_client.post(
        "/rest-auth/login/",
        {
            "username": "dummy1@dispostable.com",
            "password": "testuser1234_",
        },
        format="json",
    )
    assert response.status_code == 403
    assert response.data == {
        "detail": "There is already an active session using your account. Logout all sessions by going to /logout/all uri."
    }


def test_if_logout_all_endpoint_exists(api_client):
    response = api_client.post("/users/logout/all/")
    # as not logged in should give 401
    assert response.status_code == 401


def test_logout_all_endpoint_after_two_logins(api_client, django_user_model):
    """
    Assuming that we have to replicate logout all scenario,
    we have to login the users twice so that we get multiple sessions error,
    and then call, logout/all endpoint as without logging in one cant access
    that endpoint.
    """
    # create user
    django_user_model.objects.create_user(
        username="dummy1@dispostable.com",
        password="testuser1234_",
    )
    # first login, should be ok
    response = api_client.post(
        "/rest-auth/login/",
        {
            "username": "dummy1@dispostable.com",
            "password": "testuser1234_",
        },
        format="json",
    )
    assert response.status_code == 200
    # second login and should fail, meaning user already logged in.
    response = api_client.post(
        "/rest-auth/login/",
        {
            "username": "dummy1@dispostable.com",
            "password": "testuser1234_",
        },
        format="json",
    )
    assert response.status_code == 403
    # now call logout all, should give 200
    response = api_client.post("/users/logout/all/")
    assert response.status_code == 200
    # And, now when tried to login again it should be ok!
    response = api_client.post(
        "/rest-auth/login/",
        {
            "username": "dummy1@dispostable.com",
            "password": "testuser1234_",
        },
        format="json",
    )
    assert response.status_code == 200
