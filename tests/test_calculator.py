from unittest.mock import MagicMock, patch

from loans import calculators


def test_get_per():
    per = list(calculators.get_per(3))
    assert per == [1, 2, 3]


def test_get_interest_paid():
    kwargs = {"rate": 0.1, "per": [1, 2, 3], "nper": 3, "pv": 10_000}
    with patch("numpy_financial.ipmt", return_value=-0.333) as mock_ipmt:
        interest_paid = calculators.get_interest_paid(**kwargs)

    assert interest_paid == 0.33
    mock_ipmt.assert_called_once_with(**kwargs)


def test_get_principal_paid():
    kwargs = {"rate": 0.1, "per": [1, 2, 3], "nper": 3, "pv": 10_000}
    with patch("numpy_financial.ppmt", return_value=-2.878) as mock_ppmt:
        interest_paid = calculators.get_principal_paid(**kwargs)

    assert interest_paid == 2.88
    mock_ppmt.assert_called_once_with(**kwargs)


def test_get_balance():
    principal_paid = MagicMock()
    principal_paid.cumsum.return_value = 9_000
    balance = calculators.get_balance(10_000, principal_paid)
    assert balance == 1_000


def test_get_payment():
    assert calculators.get_payment(2.2222, 2.226) == 4.45


def test_get_loan_amortization_schedule_with_no_periods():
    assert calculators.get_amortization_schedule(0, 0, 0) == []


@patch.object(calculators, "get_interest_paid")
@patch.object(calculators, "get_principal_paid")
@patch.object(calculators, "get_balance")
@patch.object(calculators, "get_payment")
@patch.object(calculators, "get_per")
def test_get_loan_amortization_schedule(
    mock_get_per,
    mock_get_payment,
    mock_get_balance,
    mock_get_principal_paid,
    mock_get_interest_paid,
):
    kwargs = {"principal": 10_000, "rate": 0.1, "number_of_periods": 1}
    schedule = calculators.get_amortization_schedule(**kwargs)

    assert schedule == [
        {
            "balance": mock_get_balance.return_value[0],
            "interest": mock_get_interest_paid.return_value[0],
            "principal": mock_get_principal_paid.return_value[0],
            "payment": mock_get_payment.return_value[0],
        }
    ]

    mock_get_per.assert_called_once_with(1)
    per = mock_get_per.return_value
    mock_get_interest_paid.assert_called_once_with(0.1, per, 1, 10_000)
    mock_get_principal_paid.assert_called_once_with(0.1, per, 1, 10_000)
    interest = mock_get_interest_paid.return_value
    principal = mock_get_principal_paid.return_value
    mock_get_balance.assert_called_once_with(10_000, principal)
    mock_get_payment.assert_called_once_with(interest, principal)
