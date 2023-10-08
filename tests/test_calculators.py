# tests/test_calculators.py
import pytest


def get_schedule_from_calculator_api(**kwargs):
    raise NotImplementedError


def get_schedule_from_loan_admin(**kwargs):
    raise NotImplementedError


def get_schedule_sent_on_loan_create(**kwargs):
    raise NotImplementedError


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
