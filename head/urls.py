
from django.urls import path
from . import views

app_name = "head"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("review/", views.review_by_head, name="review_by_head"),
    path("completed/", views.completed_by_head, name="completed_by_head"),
    path(
        "complete/<int:invoice_id>/",
        views.complete_invoice,
        name="complete_invoice",
    ),
]
