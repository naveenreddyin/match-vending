import pytest

from rest_framework.test import APIClient


@pytest.fixture(autouse=True)
def api_client():
    return APIClient()
