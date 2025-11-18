from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("Coffee", "Coffee"),
        ("Tea", "Tea"),
        ("Special", "Special"),
    ]

    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default="Coffee"
    )

    def __str__(self):
        return self.name
