
from django.urls import path
from . import views

app_name = "mro"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("create-index/", views.create_index, name="create_index"),
    path("invoice-list/", views.invoice_list, name="invoice_list"),
    path("invoice-register/", views.invoice_register, name="invoice_register"),
    path("completed-jobs/", views.completed_jobs, name="completed_jobs"),

    path(
        "invoice-pdf/<int:invoice_id>/",
        views.convert_invoice_pdf,
        name="convert_invoice_pdf",
    ),

    path(
        "send-to-tm/<int:invoice_id>/",
        views.send_invoice_to_tm,
        name="send_invoice_to_tm",
    ),
]
