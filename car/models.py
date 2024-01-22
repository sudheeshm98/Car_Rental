from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


# Create your models here.


class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.CharField(max_length=200)
    model = models.CharField(max_length=150)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    fuel = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=20)
    image_url = models.URLField(max_length=2083, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    location = models.CharField(max_length=150, null=True)
    stars = models.DecimalField(max_digits=3, decimal_places=2, validators=[
                                MaxValueValidator(5.00)])
    availability = models.BooleanField(default=True)


class RentalHistory(models.Model):
    car = models.ForeignKey(Car, related_name='rentals',
                            on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    rental_date = models.DateTimeField()
    return_date = models.DateTimeField()
    rental_amount = models.DecimalField(
        max_digits=8, decimal_places=2, null=True)
    payment_status = models.BooleanField(default=False)
    return_status = models.BooleanField(default=False)

    def total_price(self):
        duration = self.return_date - self.rental_date
        self.rental_amount = duration.days * self.car.price
        self.save()

    def mark_as_paid(self):
        self.payment_status = True
        self.save()
