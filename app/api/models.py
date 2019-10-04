from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


class Pizza(models.Model):
    flavour = models.CharField(max_length=100)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)


class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)


class Order(models.Model):

    order_status_choices = (
        (1, _('Ordered')),
        (2, _('Processing')),
        (3, _('Delivered')),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=order_status_choices,
                                              default=1)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)

    @property
    def items(self):
        return self.item_set.all()


class Item(models.Model):
    size_choices = (
        (1, _('Small')),
        (2, _('Medium')),
        (3, _('Large')),
    )
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
                                        # validators=[MaxValueValidator(100), MinValueValidator(1)])
    size = models.PositiveSmallIntegerField(choices=size_choices,
                                            default=2)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)
