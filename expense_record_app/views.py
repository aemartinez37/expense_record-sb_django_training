from django.http import Http404
from django.shortcuts import render
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Spender, Expense


def index(request):
    spenders_list = Spender.objects.all()
    context = {'spenders_list': spenders_list}
    return render(request, 'spender/index.html', context)


def expenses_by_spender(request, spender_id):
    try:
        spender = Spender.objects.get(pk=spender_id)
    except Spender.DoesNotExist:
        raise Http404("Spender does not exist")

    expenses_list = spender.expense_set.all()
    context = {'expenses_list': expenses_list,
               'spender_name': spender.full_name}
    return render(request, 'expense/by_spender.html', context)


class SpenderListView(ListView):

    model = Spender

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class SpenderDetailView(DetailView):

    model = Spender


    def get_object(self):
        slug = self.kwargs['slug']
        try:
           d_obj = Spender.objects.get(id=int(slug))
        except Spender.DoesNotExist:
            d_obj = None
        return d_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
