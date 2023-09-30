# tests/test_admin.py
import pandas as pd
import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from pyquery import PyQuery as pq

from loans.models import Loan

pytestmark = pytest.mark.django_db


def test_admin_10_000_loan_with_3_payments_over_3_years_at_10_percent():
    user = get_user_model().objects.create(is_staff=True, is_superuser=True)
    client = Client()
    client.force_login(user)

    loan = Loan.objects.create(rate=0.1, number_of_periods=3, principal=10_000)

    response = client.get(f"/admin/loans/loan/{loan.pk}/change/")
    assert response.status_code == 200

    dom = pq(response.content)
    table = dom.find("table.schedule")
    # >>> table.text()
    #
    #   'balance\ninterest\npayment\nprincipal\n'
    #   '6978.85\n1000.00\n4021.15\n3021.15\n'
    #   ...

    # >>> tr = table.find("tr")
    # >>> tr.text_content()
    #   '\n      balance\n      interest\n      payment\n      principal\n    '

    data = [
        row.text_content().strip().replace(" ", "").split("\n")
        for row in table.find("tr")
    ]

    # [
    #   ['balance', 'interest', 'payment', 'principal'],
    #   ['6978.85', '1000.00', '4021.15', '3021.15'],
    #   ['3655.59', '697.89', '4021.15', '3323.26'],
    #   ['0.00', '365.56', '4021.15', '3655.59']
    # ]

    df = pd.DataFrame(data[1:], columns=data[0])
    #    balance interest  payment principal
    # 0  6978.85  1000.00  4021.15   3021.15
    # 1  3655.59   697.89  4021.15   3323.26
    # 2     0.00   365.56  4021.15   3655.59

    df = df.astype(float)  # Values parsed as strings, cast as floats.
    result = df.to_dict("records")

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
