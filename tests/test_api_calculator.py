# tests/test_api_calculator.py
from rest_framework.test import APIClient


def test_api_10_000_loan_with_3_payments_over_3_years_at_10_percent():
    data = {"principal": 10_000, "rate": 0.1, "number_of_periods": 3}
    client = APIClient()
    response = client.get("/calculator/", data)
    assert response.status_code == 200

    result = response.json()
    expected = [
        {
            "balance": 6_978.85,
            "interest": 1_000,
            "payment": 4_021.15,
            "principal": 3_021.15,
        },
        {
            "balance": 3_655.59,
            "interest": 697.89,
            "payment": 4_021.15,
            "principal": 3_323.26,
        },
        {
            "balance": 0,
            "interest": 365.56,
            "payment": 4_021.15,
            "principal": 3_655.59,
        },
    ]
    assert result == expected


def test_api_with_0_periods():
    data = {"principal": 10_000, "rate": 0.1, "number_of_periods": 0}

    client = APIClient()
    response = client.get("/calculator/", data)
    assert response.status_code == 200
    assert response.json() == []
