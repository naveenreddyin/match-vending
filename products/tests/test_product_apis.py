import pytest

from products.tests.factories import ProductFactory

pytestmark = pytest.mark.django_db


def test_if_get_product_url_exists(api_client):
    response = api_client.get("/products/")
    # should give 401 as unauthenticate
    assert response.status_code == 401


def test_if_get_product_url_is_success_when_authenticated(
    get_seller_user_token_and_client,
):
    _, client = get_seller_user_token_and_client
    response = client.get("/products/")
    # should give 200 as authenticated
    assert response.status_code == 200


def test_if_any_user_role_can_get_product_url_is_success_when_authenticated(
    get_any_user_token_and_client,
):
    _, client = get_any_user_token_and_client
    response = client.get("/products/")
    # should give 200 as authenticated
    assert response.status_code == 200


def test_to_create_product_when_unauthenticated(
    api_client,
):
    proxy_product = ProductFactory.build()
    response = api_client.post(
        "/products/",
        {
            "name": proxy_product.name,
        },
        format="json",
    )
    # should give 401 as unauthenticated
    assert response.status_code == 401


def test_that_only_user_with_seller_role_could_create(get_any_user_token_and_client):
    _, client = get_any_user_token_and_client
    proxy_product = ProductFactory.build()
    response = client.post(
        "/products/",
        {
            "name": proxy_product.name,
        },
        format="json",
    )
    assert response.status_code == 403


def test_for_mandatory_field_when_creation(get_seller_user_token_and_client):
    _, client = get_seller_user_token_and_client
    proxy_product = ProductFactory.build()
    response = client.post(
        "/products/",
        {
            "name": proxy_product.name,
        },
        format="json",
    )
    # should give 400 as fields missing
    assert response.status_code == 400
    assert response.data == {
        "seller": ["This field is required."],
        "amount": ["This field is required."],
        "cost": ["This field is required."],
    }


def test_product_cost_validation(get_seller_user_token_and_client):
    _, client = get_seller_user_token_and_client
    proxy_product = ProductFactory.build()
    response = client.post(
        "/products/",
        {
            "name": proxy_product.name,
            "seller": 1,
            "amount": 10,
            "cost": 11,
        },
        format="json",
    )
    # should give 400 as fields missing
    assert response.status_code == 400
    assert response.data == {"cost": ["cost is not multiple of 5"]}


def test_create_product_by_seller(get_seller_user_token_and_client):
    _, client = get_seller_user_token_and_client
    proxy_product = ProductFactory.build()
    response = client.post(
        "/products/",
        {
            "name": proxy_product.name,
            "seller": 1,
            "amount": 10,
            "cost": 10,
        },
        format="json",
    )
    # should give 201 as all requirements done
    assert response.status_code == 201


def test_that_any_user_cant_do_product_update(
    get_product, get_any_user_token_and_client
):
    _, client = get_any_user_token_and_client
    proxy_product = ProductFactory.build()
    response = client.put(
        f"/products/{get_product.id}/",
        {
            "name": proxy_product.name,
            "seller": 1,
            "amount": 10,
            "cost": 10,
        },
        format="json",
    )
    assert response.status_code == 403


def test_that_only_owner_can_update_product(get_product_and_client):
    product, client = get_product_and_client
    proxy_product = ProductFactory.build()
    response = client.put(
        f"/products/{product.id}/",
        {
            "name": proxy_product.name,
            "seller": 1,
            "amount": 10,
            "cost": 10,
        },
        format="json",
    )
    assert response.status_code == 200
