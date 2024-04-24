from django.db import models
from django.db.models import Sum, Count, F, Q
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Account(models.Model):
    """
    Represents a financial account.

    Attributes:
        name (str): The name of the account.
        balance (float): The current balance of the account.
        income (float): The total income received in the account.
        expense (float): The total expenses incurred from the account.
        user (User): The user associated with the account.
        saving_goal (float): The saving goal for the account.
        liability_list (QuerySet): The liabilities associated with the account.
        salary (float): The salary associated with the account.
    """

    name = models.CharField(max_length=100)
    balance = models.FloatField(default=0)
    income = models.FloatField(default=0)
    expense = models.FloatField(default=0)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    saving_goal = models.FloatField(default=0)
    liability_list = models.ManyToManyField("Liability", blank=True)
    salary = models.FloatField(default=0)


class Liability(models.Model):
    """
    Represents a liability in the finance manager.

    Attributes:
        name (str): The name of the liability.
        amount (float): The amount of the liability.
        date (date): The date of the liability.
        long_term (bool): Indicates if the liability is long-term.
        interest_rate (float): The interest rate of the liability.
        end_date (date): The end date of the liability.
        monthly_expense (float): The monthly expense of the liability.
        user (User): The user associated with the liability.
    """

    name = models.CharField(max_length=100)
    amount = models.FloatField(default=0)
    date = models.DateField(null=False, default=datetime.now().date())
    long_term = models.BooleanField(default=False)
    interest_rate = models.FloatField(default=0, blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    monthly_expense = models.FloatField(default=0, blank=True, null=True)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to calculate the monthly expense for long-term liabilities.

        If the liability is long-term, the monthly expense is calculated based on the interest rate and duration.
        If the liability is not long-term, the monthly expense remains unchanged.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        if self.long_term:
            self.monthly_expense = self.calculate_monthly_expense()
        super(Liability, self).save(*args, **kwargs)

    def calculate_monthly_expense(self):
        """
        Calculates the monthly expense for long-term liabilities.

        If the interest rate is 0, the monthly expense is calculated based on the duration.
        If the interest rate is not 0, the monthly expense is calculated using the interest rate formula.

        Returns:
            float: The calculated monthly expense.
        """
        if self.long_term:
            if self.interest_rate == 0:
                days = (self.end_date - self.date).days
                return self.amount / ((days) / 30)  # Assuming a month has 30 days
            else:
                months = (
                    (self.end_date.year - datetime.now().year) * 12
                    + self.end_date.month
                    - datetime.now().month
                )
                monthly_rate = self.interest_rate / 12 / 100
                monthly_expense = (self.amount * monthly_rate) / (
                    1 - (1 + monthly_rate) ** -months
                )
                return round(monthly_expense, 2)
        else:
            return self.monthly_expense
