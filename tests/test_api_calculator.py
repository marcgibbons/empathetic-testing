# tests/test_api_calculator.py
from unittest.mock import patch

from django.test import RequestFactory
from loans.views import calculator


@patch("loans.views.get_amortization_schedule")
def test_calculator_api(mock):
    rf = RequestFactory()
    data = {"principal": 10_000, "rate": 0.1, "number_of_periods": 3}
    request = rf.get("/schedule/", data)
    response = calculator(request)

    mock.assert_called_once_with(**data)
    assert response.status_code == 200
    assert response.data == mock.return_value
