from factory import Faker
from factory.django import DjangoModelFactory

from products.models import Product


class ProductFactory(DjangoModelFactory):

    name = Faker("name")

    class Meta:
        model = Product
