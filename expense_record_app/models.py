from django.db import models

# Create your models here.


class Spender(models.Model):
    nickname = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.nickname
