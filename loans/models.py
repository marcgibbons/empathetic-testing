from django.db import models


class Loan(models.Model):
    """
    A model representing a loan.

    In this simple implementation, loans are paid annually.
    """

    number_of_periods = models.PositiveSmallIntegerField(
        help_text="Number of payments (years)",
    )
    principal = models.FloatField(help_text="Opening loan principal")
    rate = models.FloatField(help_text="Rate per period")
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"${self.principal:,.2f} – {self.number_of_periods} years at "
            f"{self.rate:.3%}"
        )
