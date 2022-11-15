from django.http import Http404
from django.shortcuts import render

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
