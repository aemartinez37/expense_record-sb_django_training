import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Expense


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
