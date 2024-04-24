from django.shortcuts import render, redirect


from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .models import Account, Liability
from .forms import LiabilityForm
from django.views.generic.edit import FormView

from django.utils.safestring import mark_safe

from dateutil.relativedelta import relativedelta
import plotly.express as px
from plotly.graph_objs import *


def home(request):
    user = request.user
    if user.is_authenticated:
        return redirect("expenses")
    else:
        return render(request, "fin_manager/home.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def generate_graph(data):
    """
    Generate a bar graph of monthly expenses.

    Args:
        data (pandas.DataFrame): The data containing the monthly expenses.

    Returns:
        str: The JSON representation of the generated graph.

    """
    fig = px.bar(data, x="months", y="expenses", title="Monthly Expenses")
    fig.update_layout(
        xaxis=dict(rangeslider=dict(visible=True)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="rgba(0,0,0,1)",
    )
    fig.update_traces(marker_color="#008c41")

    graph_json = fig.to_json()

    return graph_json


class ExpenseListView(FormView):
    """
    A view that displays a form for creating a new liability expense and
    renders the expense list along with aggregated data and a graph.

    Inherits from FormView class.
    """

    template_name = "expenses/expense_list.html"
    form_class = LiabilityForm
    success_url = "/"

    def form_valid(self, form):
        """
        Saves the liability expense to the database and associates it with the user's account.

        Args:
            form: The validated form containing the liability expense data.

        Returns:
            The response from the parent class's form_valid method.
        """
        account, _ = Account.objects.get_or_create(user=self.request.user)

        liability = Liability(
            name=form.cleaned_data["name"],
            amount=form.cleaned_data["amount"],
            interest_rate=form.cleaned_data["interest_rate"],
            date=form.cleaned_data["date"],
            end_date=form.cleaned_data["end_date"],
            long_term=form.cleaned_data["long_term"],
            user=self.request.user,
        )
        liability.save()
        account.liability_list.add(liability)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to be used in the template.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            The context data dictionary.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        accounts = Account.objects.filter(user=user)
        expense_data_graph = {}
        expense_data = {}

        for account in accounts:
            liabilities = account.liability_list.all()
            for liability in liabilities:
                if liability.long_term and liability.monthly_expense:
                    current_date = liability.date
                    while current_date <= liability.end_date:
                        year_month = current_date.strftime("%Y-%m")
                        if year_month not in expense_data_graph:
                            expense_data_graph[year_month] = []

                        expense_data_graph[year_month].append(
                            {
                                "name": liability.name,
                                "amount": liability.monthly_expense,
                                "date": current_date,
                                "end_date": liability.end_date,
                            }
                        )

                        # Move to the next month
                        current_date = current_date + relativedelta(months=1)
                else:
                    year_month = liability.date.strftime("%Y-%m")
                    if year_month not in expense_data_graph:
                        expense_data_graph[year_month] = []

                    expense_data_graph[year_month].append(
                        {
                            "name": liability.name,
                            "amount": liability.amount,
                            "date": liability.date,
                        }
                    )

        for account in accounts:
            liabilities = account.liability_list.all()
            for liability in liabilities:
                if liability.long_term and liability.monthly_expense:
                    current_date = liability.date
                    year_month = current_date.strftime("%Y-%m")
                    if year_month not in expense_data:
                        expense_data[year_month] = []

                    expense_data[year_month].append(
                        {
                            "name": liability.name,
                            "amount": liability.monthly_expense,
                            "date": current_date,
                            "end_date": liability.end_date,
                            "long_term": liability.long_term,
                        }
                    )

                    # Move to the next month
                    current_date = current_date + relativedelta(months=1)
                else:
                    year_month = liability.date.strftime("%Y-%m")
                    if year_month not in expense_data:
                        expense_data[year_month] = []

                    expense_data[year_month].append(
                        {
                            "name": liability.name,
                            "amount": liability.amount,
                            "date": liability.date,
                        }
                    )
        # Convert the expense_data_graph into aggregated_data
        aggregated_data = [
            {"year_month": key, "expenses": sum(item["amount"] for item in value)}
            for key, value in expense_data_graph.items()
        ]

        context["expense_data"] = expense_data
        context["aggregated_data"] = aggregated_data

        # Prepare graph_data for generating the Plotly graph
        graph_data = {
            "months": [item["year_month"] for item in aggregated_data],
            "expenses": [item["expenses"] for item in aggregated_data],
        }
        graph_data["chart"] = generate_graph(graph_data)
        context["graph_data"] = mark_safe(
            graph_data["chart"]
        )  # Use mark_safe to render the JSON as HTML

        return context
