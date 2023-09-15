from unittest.mock import patch

from django.contrib import admin

from loans.admin import LoanAdmin
from loans.models import Loan


@patch("loans.calculators.get_amortization_schedule")
@patch("pandas.DataFrame.from_dict")
def test_admin_change_view_renders_schedule(dataframe_mock, schedule_mock):
    expected = "<div>schedule</div>"
    to_html = dataframe_mock.return_value.to_html
    to_html.return_value = expected

    loan_admin = LoanAdmin(Loan, admin.site)
    loan = Loan()

    result = loan_admin.amortization_schedule(loan)
    assert result == expected

    schedule_mock.assert_called_once_with(
        number_of_periods=loan.number_of_periods,
        principal=loan.principal,
        rate=loan.rate,
    )
    dataframe_mock.assert_called_once_with(schedule_mock.return_value)
