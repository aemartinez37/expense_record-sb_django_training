from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Spender, Expense
from .forms import ExpenseForm


def index(request):
    return render(request, 'index.html')


def expenses_by_spender(request, spender_id):
    try:
        spender = Spender.objects.get(pk=spender_id)
    except Spender.DoesNotExist:
        raise Http404("Spender does not exist")

    expenses_list = spender.expense_set.all()
    context = {'expenses_list': expenses_list,
               'spender_name': spender.full_name,
               'spender_id': spender_id}
    return render(request, 'expense/by_spender.html', context)


def expense_form(request, spender_id):
    try:
        spender_obj = Spender.objects.get(pk=spender_id)
    except Spender.DoesNotExist:
        raise Http404("Spender does not exist")

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            description_data = form.cleaned_data["description"]
            value_data = form.cleaned_data["value"]
            spending_date_data = form.cleaned_data["spending_date"]

            new_expense = Expense(spender=spender_obj, description=description_data.upper(),
                                  value=value_data, spending_date=spending_date_data)

            new_expense.save()

            return HttpResponseRedirect(f"/expenses/spender/{spender_id}/")

    else:
        form = ExpenseForm()

    context = {"form": form, "spender_id": spender_id,
               "spender_nickname": spender_obj.nickname}

    return render(request, "expense/new_expense.html", context)


class SpenderListView(ListView):

    model = Spender

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class SpenderDetailView(DetailView):

    model = Spender
    slug_field = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ExpenseListView(ListView):

    template_name = 'expense_record_app/expense_list.html'
    context_object_name = 'expenses_list'

    def get_queryset(self):
        """
        Return all expenses (not including those set to be
        spent in the future).
        """
        return Expense.objects.filter(
            spending_date__lte=timezone.now()
        ).order_by('-spending_date')
