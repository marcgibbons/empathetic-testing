# tests/test_calculators.py
import json
import pandas as pd
import pytest
import responses
from django.contrib.auth import get_user_model
from django.test import Client
from pyquery import PyQuery as pq
from rest_framework.test import APIClient

from loans.models import Loan

pytestmark = pytest.mark.django_db


def get_schedule_from_calculator_api(**kwargs):
    client = APIClient()
    response = client.get("/calculator/", data=kwargs)
    assert response.status_code == 200
    return response.json()


def get_schedule_from_loan_admin(**kwargs):
    user = get_user_model().objects.create(is_staff=True, is_superuser=True)
    client = Client()
    client.force_login(user)
    loan = Loan.objects.create(**kwargs)

    response = client.get(f"/admin/loans/loan/{loan.pk}/change/")
    assert response.status_code == 200

    dom = pq(response.content)
    table = dom.find("table.schedule")
    data = [
        row.text_content().strip().replace(" ", "").split("\n")
        for row in table.find("tr")
    ]
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df.astype(float)  # Values parsed as strings, cast as floats.
    return df.to_dict("records")


@responses.activate
def get_schedule_sent_on_loan_create(**kwargs):
    responses.post("https://notifications.test")  # Register HTTP call

    client = APIClient()
    data = {"principal": 10_000, "rate": 0.1, "number_of_periods": 3}
    response = client.post("/loans/", data)
    assert response.status_code == 201

    assert responses.calls, "Expected HTTP call"
    request = responses.calls[0].request  # Grab first (and only) request
    sent_data = json.loads(request.body)
    return sent_data["schedule"]


@pytest.mark.parametrize(
    "get_schedule",
    [
        get_schedule_from_calculator_api,
        get_schedule_from_loan_admin,
        get_schedule_sent_on_loan_create,
    ],
)
def test_10_000_loan_with_3_payments_over_3_years_at_10_percent(get_schedule):
    schedule = get_schedule(principal=10_000, rate=0.1, number_of_periods=3)
    assert schedule == [
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
