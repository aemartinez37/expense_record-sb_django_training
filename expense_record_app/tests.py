import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Expense, Spender


def create_expense(description_text, days):
    """
    Create a expense for a dummy spender with the given `description_text` and spent in the
    given number of `days` offset to now (negative for expenses
    in the past, positive for future expenses).
    """
    dummy_spender = Spender.objects.create(nickname='dummy01', full_name='Dummy Spender', email='dummy@test.com')
    date = timezone.now() + datetime.timedelta(days=days)
    return Expense.objects.create(spender=dummy_spender, description=description_text, spending_date=date, value=1)


class ExpenseModelTests(TestCase):

    def test_is_recent_expense_with_future_expense(self):
        """
        is_recent_expense() returns False for expenses whose spending_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_expense = Expense(spending_date=time)
        self.assertIs(future_expense.is_recent_expense(), False)

    def test_is_recent_expense_with_old_expense(self):
        """
        is_recent_expense() returns False for expenses whose spending_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_expense = Expense(spending_date=time)
        self.assertIs(old_expense.is_recent_expense(), False)

    def test_is_recent_expense_with_recent_expense(self):
        """
        is_recent_expense() returns True for expenses whose spending_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_expense = Expense(spending_date=time)
        self.assertIs(recent_expense.is_recent_expense(), True)


class ExpensesListViewTests(TestCase):
    def test_no_expenses(self):
        """
        If no expenses exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('expense_record:expenses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No expenses registered.")
        self.assertQuerysetEqual(response.context['expenses_list'], [])

    def test_past_expense(self):
        """
        Expenses with a spending_date in the past are displayed on the
        expenses page.
        """
        expense = create_expense(description_text="Past expense", days=-30)
        response = self.client.get(reverse('expense_record:expenses'))
        self.assertQuerysetEqual(
            response.context['expenses_list'],
            [expense],
        )

    def test_future_expense(self):
        """
        Expenses with a spending_date in the future aren't displayed on
        the expenses page.
        """
        create_expense(description_text="Future expense.", days=30)
        response = self.client.get(reverse('expense_record:expenses'))
        self.assertContains(response, "No expenses registered.")
        self.assertQuerysetEqual(response.context['expenses_list'], [])

    def test_future_expense_and_past_expense(self):
        """
        Even if both past and future expenses exist, only past expenses
        are displayed.
        """
        expense = create_expense(description_text="Past expense.", days=-30)
        create_expense(description_text="Future expense.", days=30)
        response = self.client.get(reverse('expense_record:expenses'))
        self.assertQuerysetEqual(
            response.context['expenses_list'],
            [expense],
        )

    def test_two_past_expenses(self):
        """
        The expenses page may display multiple expenses.
        """
        expense1 = create_expense(description_text="Past expense 1.", days=-30)
        expense2 = create_expense(description_text="Past expense 2.", days=-5)
        response = self.client.get(reverse('expense_record:expenses'))
        self.assertQuerysetEqual(
            response.context['expenses_list'],
            [expense2, expense1],
        )
