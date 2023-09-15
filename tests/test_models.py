from loans.models import Loan


def test_str():
    loan = Loan(rate=0.1, number_of_periods=12, principal=100)
    assert str(loan) == "$100.00 – 12 years at 10.000%"
