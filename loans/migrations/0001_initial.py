from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Loan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "number_of_periods",
                    models.PositiveSmallIntegerField(
                        help_text="Number of payments (years)"
                    ),
                ),
                ("principal", models.FloatField(help_text="Opening loan principal")),
                ("rate", models.FloatField(help_text="Rate per period")),
                ("created_datetime", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
