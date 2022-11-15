from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('expenses/<int:spender_id>/',
         views.expenses_by_spender, name='expenses-by-spender'),
]
