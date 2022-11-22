from django.urls import path

from . import views
from .views import SpenderListView, SpenderDetailView, ExpenseListView

app_name = 'expense_record'
urlpatterns = [
    path('', views.index, name='index'),
    path('spenders/', SpenderListView.as_view(), name='spenders'),
    path('spender/<slug:slug>/', SpenderDetailView.as_view(), name='detail'),
    path('expenses/', ExpenseListView.as_view(), name='expenses'),
    path('expenses/spender/<int:spender_id>/',
         views.expenses_by_spender, name='expenses-by-spender'),
    path('expenses/spender/new/<int:spender_id>/',
         views.expense_form, name='expenses-new'),
]
