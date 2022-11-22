from django import forms


class ExpenseForm(forms.Form):
    description = forms.CharField(label='Description', max_length=200)
    value = forms.DecimalField(label='Value', max_digits=7, decimal_places=2)
    spending_date = forms.DateField(label='Date', widget=forms.widgets.DateInput(attrs={'type': 'date'}))
