# tests/test_api_loans.py
from unittest.mock import patch

from django.http import QueryDict
from django.test import RequestFactory

from loans.views import loans as loans_view


@patch("loans.views.requests")
@patch("loans.views.get_amortization_schedule")
@patch("loans.views.LoanSerializer")
def test_create_loans_api(serializer_mock, amort_mock, requests_mock):
    rf = RequestFactory()
    data = {"principal": "10000", "rate": "0.1"}
    request = rf.post("/calculator/", data)
    response = loans_view(request)

    assert response.status_code == 201  # Success!
    assert response.data == serializer_mock.return_value.data

    # Django transforms the query params into a QueryDict
    query_dict = QueryDict(mutable=True)
    query_dict.update(data)

    # Serializer was instantiated with the data
    serializer_mock.assert_called_once_with(data=query_dict)

    # Test that the object is saved
    save = serializer_mock.return_value.save
    save.assert_called_once_with()
    loan = save.return_value

    # Test that the notification is sent with the schedule
    requests_mock.post.assert_called_once_with(
        "https://notifications.test",
        json={
            "loan_id": loan.pk,
            "created_datetime": loan.created_datetime,
            "schedule": amort_mock.return_value,
        },
    )
