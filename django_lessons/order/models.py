from decimal import Decimal

from django.db import models

from accounts.models import StudentUser


class Product(models.Model):

    CURRENCIES = [
        ("PLN", "PLN"),
        ("USD", "USD"),
    ]

    name = models.CharField(max_length=255, 
                            null=False, 
                            blank=False)
    price = models.DecimalField(decimal_places=2, 
                                max_digits=10)
    currency = models.CharField(max_length=20,
                                choices=CURRENCIES)
    stripe_product_id = models.CharField(max_length=255,
                                help_text="ID of a product created on the stripe site to identify product",
                                null=False, 
                                blank=False)

    def __str__(self) -> str:
        return f"Product {self.name}"

    def get_display_price(self):
        return self.price * Decimal(100)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(price__gt=Decimal('0')), 
                                   name='price_gt_0')
        ]

class Order(models.Model):

    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Order for Product {self.product.name} by {self.student.first_name} {self.student.last_name}"
