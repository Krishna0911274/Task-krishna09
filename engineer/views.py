
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from mro.models import ClientInvoice


def is_engineer(user):
    return (
        user.is_authenticated
        and user.groups.filter(name="Engineer").exists()
    )


@login_required
@user_passes_test(is_engineer, login_url="login")
def dashboard(request):
    pending_count = ClientInvoice.objects.filter(
        workflow_status="waiting_engineer"
    ).count()

    completed_count = ClientInvoice.objects.filter(
        workflow_status="completed_engineer"
    ).count()

    return render(
        request,
        "engineer/engineer_dashboard.html",
        {
            "active_page": "dashboard",
            "page_title": "Engineer Dashboard",
            "pending_count": pending_count,
            "completed_count": completed_count,
        },
    )


@login_required
@user_passes_test(is_engineer, login_url="login")
def review_by_engineer(request):
    invoices = ClientInvoice.objects.filter(
        workflow_status="waiting_engineer"
    ).order_by("-created_at")

    return render(
        request,
        "engineer/engineer_dashboard.html",
        {
            "active_page": "review_by_engineer",
            "page_title": "Review by Engineer",
            "invoices": invoices,
        },
    )


@login_required
@user_passes_test(is_engineer, login_url="login")
def review_invoice(request, invoice_id):
    invoice = get_object_or_404(
        ClientInvoice,
        id=invoice_id,
        workflow_status="waiting_engineer",
    )

    if request.method == "POST":
        client_name = request.POST.get("client_name", "").strip()
        contact_number = request.POST.get("contact_number", "").strip()
        gender = request.POST.get("gender", "")
        product_name = request.POST.get("product_name", "").strip()
        serial_number = request.POST.get("serial_number", "").strip()
        purchase_date = request.POST.get("purchase_date", "")

        yes_no_fields = [
            "under_warranty",
            "installed",
            "issue_reported",
            "proof_of_purchase",
        ]

        required_values = [
            client_name,
            contact_number,
            gender,
            product_name,
            serial_number,
            purchase_date,
        ]

        if not all(required_values):
            messages.error(request, "Please complete all fields.")

        elif gender not in dict(ClientInvoice.GENDER_CHOICES):
            messages.error(request, "Please select a valid gender.")

        elif len(client_name) > 100 or len(contact_number) > 15:
            messages.error(
                request,
                "Client name or contact number is too long.",
            )

        elif len(product_name) > 150 or len(serial_number) > 100:
            messages.error(
                request,
                "Product name or serial number is too long.",
            )

        elif any(
            request.POST.get(field) not in ("Yes", "No")
            for field in yes_no_fields
        ):
            messages.error(
                request,
                "Please answer all product questions.",
            )

        else:
            try:
                parsed_date = date.fromisoformat(purchase_date)

                invoice.client_name = client_name
                invoice.contact_number = contact_number
                invoice.gender = gender
                invoice.product_name = product_name
                invoice.serial_number = serial_number
                invoice.purchase_date = parsed_date

                for field in yes_no_fields:
                    setattr(
                        invoice,
                        field,
                        request.POST.get(field) == "Yes",
                    )

                invoice.workflow_status = "completed_engineer"
                invoice.save()

                messages.success(
                    request,
                    f"Invoice #{invoice.id} completed successfully.",
                )
                return redirect("engineer:completed_by_engineer")

            except (ValueError, OverflowError):
                messages.error(
                    request,
                    "Please enter a valid purchase date.",
                )

    return render(
        request,
        "engineer/engineer_dashboard.html",
        {
            "active_page": "review_invoice",
            "page_title": "Review Invoice",
            "invoice": invoice,
        },
    )


@login_required
@user_passes_test(is_engineer, login_url="login")
def completed_by_engineer(request):
    invoices = ClientInvoice.objects.filter(
        workflow_status="completed_engineer"
    ).order_by("-created_at")

    return render(
        request,
        "engineer/engineer_dashboard.html",
        {
            "active_page": "completed_by_engineer",
            "page_title": "Completed by Engineer",
            "invoices": invoices,
        },
    )


@login_required
@user_passes_test(is_engineer, login_url="login")
@require_POST
def send_to_head(request, invoice_id):
    invoice = get_object_or_404(
        ClientInvoice,
        id=invoice_id,
        workflow_status="completed_engineer",
    )

    invoice.workflow_status = "waiting_head"
    invoice.save(update_fields=["workflow_status"])

    messages.success(
        request,
        f"Invoice #{invoice.id} sent to Head successfully!",
    )

    return redirect("engineer:completed_by_engineer")
