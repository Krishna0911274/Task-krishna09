
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from mro.models import ClientInvoice


def is_head(user):
    return user.is_authenticated and user.groups.filter(name="Head").exists()


@login_required
@user_passes_test(is_head, login_url="login")
def dashboard(request):
    pending_count = ClientInvoice.objects.filter(
        workflow_status="waiting_head"
    ).count()

    completed_count = ClientInvoice.objects.filter(
        workflow_status="completed"
    ).count()

    return render(request, "head/head_dashboard.html", {
        "active_page": "dashboard",
        "page_title": "Head Dashboard",
        "pending_count": pending_count,
        "completed_count": completed_count,
    })


@login_required
@user_passes_test(is_head, login_url="login")
def review_by_head(request):
    invoices = ClientInvoice.objects.filter(
        workflow_status="waiting_head"
    ).order_by("-created_at")

    return render(request, "head/head_dashboard.html", {
        "active_page": "review_by_head",
        "page_title": "Review by Head",
        "invoices": invoices,
    })


@login_required
@user_passes_test(is_head, login_url="login")
def completed_by_head(request):
    invoices = ClientInvoice.objects.filter(
        workflow_status="completed"
    ).order_by("-created_at")

    return render(request, "head/head_dashboard.html", {
        "active_page": "completed_by_head",
        "page_title": "Completed by Head",
        "invoices": invoices,
    })


@login_required
@user_passes_test(is_head, login_url="login")
@require_POST
def complete_invoice(request, invoice_id):
    invoice = get_object_or_404(
        ClientInvoice,
        id=invoice_id,
        workflow_status="waiting_head",
    )

    invoice.workflow_status = "completed"
    invoice.save(update_fields=["workflow_status"])

    messages.success(
        request,
        f"Invoice #{invoice.id} completed successfully!"
    )

    return redirect("head:completed_by_head")
