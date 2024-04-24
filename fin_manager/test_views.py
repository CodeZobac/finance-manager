from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from .models import Account, Liability
from .forms import LiabilityForm


class ExpenseListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")
        self.account = Account.objects.create(user=self.user)
        self.liability = Liability.objects.create(
            name="Test Liability",
            amount=1000,
            interest_rate=0.05,
            date=date.today(),
            end_date=date.today() + relativedelta(months=12),
            long_term=True,
            monthly_expense=100,
            user=self.user,
        )

    def test_form_valid(self):
        form_data = {
            "name": "New Liability",
            "amount": 2000,
            "interest_rate": 0.1,
            "date": date.today(),
            "end_date": date.today() + relativedelta(months=24),
            "long_term": True,
        }
        response = self.client.post(reverse("expense-list"), data=form_data)
        self.assertEqual(
            response.status_code, 302
        )  # Check if the form submission redirects
        self.assertEqual(
            Liability.objects.count(), 2
        )  # Check if a new liability is created
        new_liability = Liability.objects.latest("id")
        self.assertEqual(
            new_liability.name, form_data["name"]
        )  # Check if the new liability has the correct name
        self.assertEqual(
            new_liability.amount, form_data["amount"]
        )  # Check if the new liability has the correct amount

    def test_get_context_data(self):
        response = self.client.get(reverse("expense-list"))
        self.assertEqual(
            response.status_code, 200
        )  # Check if the view returns a successful response
        context = response.context
        self.assertIn(
            "expense_data", context
        )  # Check if the context contains 'expense_data'
        self.assertIn(
            "aggregated_data", context
        )  # Check if the context contains 'aggregated_data'
        self.assertIn(
            "graph_data", context
        )  # Check if the context contains 'graph_data'
        self.assertEqual(
            len(context["expense_data"]), 1
        )  # Check if the expense_data has the correct length
        self.assertEqual(
            len(context["aggregated_data"]), 1
        )  # Check if the aggregated_data has the correct length
        self.assertEqual(
            len(context["graph_data"]["months"]), 1
        )  # Check if the graph_data has the correct length

        # You can add more assertions to check the correctness of the context dataimport datetime


from django.test import TestCase
from django.contrib.auth.models import User
from fin_manager.models import Account, Liability
from fin_manager.views import YourViewClass


class YourViewClassTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.account = Account.objects.create(user=self.user)
        self.liability = Liability.objects.create(
            account=self.account,
            name="Test Liability",
            amount=100,
            date=datetime.date.today(),
            long_term=True,
            monthly_expense=True,
            end_date=datetime.date.today() + datetime.timedelta(days=30),
        )

    def test_get_context_data(self):
        view = YourViewClass()
        view.request = self.client.get("/").wsgi_request
        view.kwargs = {}  # Add any required kwargs here

        context = view.get_context_data()

        # Assert that the context contains the expected keys
        self.assertIn("expense_data", context)
        self.assertIn("aggregated_data", context)
        self.assertIn("graph_data", context)

        # Assert that the expense_data is correctly populated
        self.assertEqual(len(context["expense_data"]), 1)
        self.assertEqual(
            context["expense_data"]["YYYY-MM"][0]["name"], "Test Liability"
        )
        self.assertEqual(context["expense_data"]["YYYY-MM"][0]["amount"], 100)

        # Assert that the aggregated_data is correctly populated
        self.assertEqual(len(context["aggregated_data"]), 1)
        self.assertEqual(context["aggregated_data"][0]["year_month"], "YYYY-MM")
        self.assertEqual(context["aggregated_data"][0]["expenses"], 100)

        # Assert that the graph_data is correctly populated
        self.assertEqual(len(context["graph_data"]["months"]), 1)
        self.assertEqual(context["graph_data"]["months"][0], "YYYY-MM")
        self.assertEqual(len(context["graph_data"]["expenses"]), 1)
        self.assertEqual(context["graph_data"]["expenses"][0], 100)
