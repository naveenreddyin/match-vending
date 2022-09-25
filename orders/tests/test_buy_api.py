import pytest

from users.models import Profile

pytestmark = pytest.mark.django_db


def test_if_buy_url_exists(api_client):
    response = api_client.post("/buy/")
    assert response.status_code == 401


def test_buy_endpoint_get_method(api_client):
    response = api_client.get("/buy/")
    assert response.status_code == 401


def test_buy_endpoint_put_method(api_client):
    response = api_client.put("/buy/")
    assert response.status_code == 401


def test_buy_endpoint_delete_method(api_client):
    response = api_client.delete("/buy/")
    assert response.status_code == 401


def test_only_buyer_role_can_post(get_any_user_token_and_client):
    _, client = get_any_user_token_and_client
    response = client.post("/buy/")
    assert response.status_code == 403


def test_buyer_role_can_post_but_no_data(get_buyer_user_token_and_client):
    _, client = get_buyer_user_token_and_client
    response = client.post("/buy/")
    assert response.status_code == 400


def test_buyer_role_can_post_but_right_data(get_buyer_user_product_and_client):
    user, product, client = get_buyer_user_product_and_client()

    assert user.user_profile.deposit == 100

    response = client.post(
        "/buy/",
        {
            "product": product.id,
            "amount": 10,
        },
    )
    assert response.status_code == 201
    product.refresh_from_db()
    assert product.amount == 0

    # check user balance
    user.refresh_from_db()
    assert user.user_profile.deposit == 0


def test_buyer_cant_buy_if_no_or_low_balance(get_buyer_user_product_and_client):
    _, product, client = get_buyer_user_product_and_client(deposit=5)
    response = client.post(
        "/buy/",
        {
            "product": product.id,
            "amount": 10,
        },
    )
    assert response.status_code == 400
    assert response.data == ["your balance is low."]


def test_buyer_with_no_amount(get_buyer_user_product_and_client):
    _, product, client = get_buyer_user_product_and_client()
    response = client.post(
        "/buy/",
        {
            "product": product.id,
        },
    )
    assert response.status_code == 400
