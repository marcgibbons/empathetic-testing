from django.contrib import admin
from django.utils.html import format_html

from . import calculators, models


@admin.register(models.Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "principal",
        "rate",
        "number_of_periods",
        "created_datetime",
    ]

    fields = [
        "principal",
        "rate",
        "number_of_periods",
        "amortization_schedule",
    ]
    readonly_fields = ["amortization_schedule"]

    @admin.display
    def amortization_schedule(self, obj):
        df = calculators.get_amortization_schedule(
            principal=obj.principal,
            number_of_periods=obj.number_of_periods,
            rate=obj.rate,
        )
        return format_html(df.to_html(index=False, classes=["schedule"]))
