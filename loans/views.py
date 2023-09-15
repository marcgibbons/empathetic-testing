import requests
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .calculators import get_amortization_schedule
from .models import Loan


class ScheduleParamSerializer(serializers.Serializer):
    rate = serializers.FloatField(min_value=0, max_value=1)
    principal = serializers.FloatField()
    number_of_periods = serializers.IntegerField(min_value=0)


@api_view(http_method_names=["GET"])
def calculator(request):
    serializer = ScheduleParamSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    data = get_amortization_schedule(**serializer.data)

    return Response(data)


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "id",
            "number_of_periods",
            "principal",
            "rate",
        ]


@api_view(http_method_names=["POST"])
def loans(request):
    serializer = LoanSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    loan = serializer.save()

    schedule = get_amortization_schedule(
        principal=loan.principal,
        number_of_periods=loan.number_of_periods,
        rate=loan.rate,
    )
    requests.post(
        "https://notifications.test",
        json={
            "loan_id": loan.pk,
            "schedule": schedule,
            "created_datetime": loan.created_datetime,
        },
    )

    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
