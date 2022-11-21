from django.urls import path

from . import views
from .views import SpenderListView, SpenderDetailView

urlpatterns = [
    path('', SpenderListView.as_view(), name='spender-list'),
    path('<slug:slug>/', SpenderDetailView.as_view(), name='spender-detail'),
    path('expenses/<int:spender_id>/',
         views.expenses_by_spender, name='expenses-by-spender'),
]
