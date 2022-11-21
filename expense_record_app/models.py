from django.db import models

# Create your models here.


class Spender(models.Model):
    nickname = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.nickname


class Expense(models.Model):
    spender = models.ForeignKey(Spender, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    value = models.DecimalField(max_digits=7, decimal_places=2)
    spending_date = models.DateField('date of spending')

    def __str__(self):
        return self.description
