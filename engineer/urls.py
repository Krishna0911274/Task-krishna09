
from django.urls import path
from . import views

app_name = "engineer"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("review/", views.review_by_engineer, name="review_by_engineer"),
    path(
        "review/<int:invoice_id>/",
        views.review_invoice,
        name="review_invoice",
    ),
    path(
        "completed/",
        views.completed_by_engineer,
        name="completed_by_engineer",
    ),
    
    path(
        "send-to-head/<int:invoice_id>/",
        views.send_to_head,
        name="send_to_head",
    ),

]
