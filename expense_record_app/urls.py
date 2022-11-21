from django.urls import path

from . import views
from .views import SpenderListView, SpenderDetailView

app_name = 'expense_record'
urlpatterns = [
    path('', SpenderListView.as_view(), name='spenders'),
    path('<slug:slug>/', SpenderDetailView.as_view(), name='detail'),
    path('expenses/<int:spender_id>/',
         views.expenses_by_spender, name='expenses'),
]
