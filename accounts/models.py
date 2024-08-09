from django.db import models
from django.core.validators import MinLengthValidator

class Person(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    ssn = models.CharField(max_length=10, validators=[MinLengthValidator(10)])

class Account(models.Model):
    balance = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(Person, on_delete=models.PROTECT)
    class Meta:
        indexes = [
            models.Index(fields=['balance'])
        ]