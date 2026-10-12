
from django.urls import path
from . import views

app_name = "tm"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("review/", views.review_by_tm, name="review_by_tm"),
    path(
        "review/<int:invoice_id>/",
        views.review_invoice,
        name="review_invoice",
    ),
    path("completed/", views.completed_by_tm, name="completed_by_tm"),
    path("send-to-engineer/<int:invoice_id>/",views.send_to_engineer,name="send_to_engineer"),
]
