from django.db import models
from django.conf import settings


class Product(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="seller",
    )
    amount = models.PositiveIntegerField()
    cost = models.PositiveIntegerField()
    name = models.CharField(
        max_length=50,
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self) -> str:
        return f"user : {self.seller}, product: {self.name} "
