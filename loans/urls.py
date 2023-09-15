from django.urls import path

from . import views

urlpatterns = [
    path("calculator/", views.calculator, name="calculator"),
    path("loans/", views.loans, name="loans"),
]
