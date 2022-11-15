from django.contrib import admin
from .models import Spender, Expense

# Register your models here.

admin.site.register(Spender)
admin.site.register(Expense)
