# tests/test_api_loans.py
import pytest
import responses
from rest_framework.test import APIClient

from loans.models import Loan

pytestmark = pytest.mark.django_db


@responses.activate
def test_create_loans_api():
    client = APIClient()
    data = {
        "principal": 10_000,
        "rate": 0.1,
        "number_of_periods": 3,
    }
    response = client.post("/loans/", data)
    assert response.status_code == 201

    result = response.json()
    loan = Loan.objects.get(pk=result["id"])

    schedule = [
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


