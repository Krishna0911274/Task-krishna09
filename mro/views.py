
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import ClientInvoice
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST




def is_mro(user):
    return user.is_authenticated and user.groups.filter(name="MRO").exists()


@login_required
@user_passes_test(is_mro, login_url="login")
def dashboard(request):
    return render_page(request, "dashboard", "MRO Dashboard")


@login_required
@user_passes_test(is_mro, login_url="login")
def create_index(request):
    return render_page(request, "create_index", "Create Index")



@login_required
@user_passes_test(is_mro, login_url="login")
def invoice_list(request):
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
            client_name, contact_number, gender,
            product_name, serial_number, purchase_date,
        ]

        if not all(required_values) or any(
            request.POST.get(field) not in ("Yes", "No")
            for field in yes_no_fields
        ):
            messages.error(request, "Please complete all fields correctly.")
        else:
            try:
                from datetime import date

                parsed_date = date.fromisoformat(purchase_date)

                if gender not in dict(ClientInvoice.GENDER_CHOICES):
                    raise ValueError("Invalid gender")

                if len(contact_number) > 15:
                    raise ValueError("Invalid contact number")

                ClientInvoice.objects.create(
                    client_name=client_name,
                    contact_number=contact_number,
                    gender=gender,
                    product_name=product_name,
                    serial_number=serial_number,
                    purchase_date=parsed_date,
                    under_warranty=request.POST["under_warranty"] == "Yes",
                    installed=request.POST["installed"] == "Yes",
                    issue_reported=request.POST["issue_reported"] == "Yes",
                    proof_of_purchase=request.POST["proof_of_purchase"] == "Yes",
                )

                messages.success(request, "Client information saved successfully!")
                return redirect("mro:invoice_list")

            except (ValueError, OverflowError):
                messages.error(request, "Please enter valid information.")

    return render(
    request,
    "mro/mro_dashboard.html",
    {
        "active_page": "invoice_list",
        "page_title": "Invoice List",
        "yes_no_questions": [
            ("under_warranty", "7. Is the product under warranty?"),
            ("installed", "8. Has the product been installed?"),
            ("issue_reported", "9. Has the client reported an issue?"),
            ("proof_of_purchase", "10. Is proof of purchase available?"),
        ],
    },
)


@login_required
@user_passes_test(is_mro, login_url="login")
def invoice_register(request):
    invoices = ClientInvoice.objects.all().order_by("-created_at")

    return render(
        request,
        "mro/mro_dashboard.html",
        {
            "active_page": "invoice_register",
            "page_title": "Invoice Register",
            "invoices": invoices,
        },
    )


@login_required
@user_passes_test(is_mro, login_url="login")
def completed_jobs(request):
    return render_page(request, "completed_jobs", "Completed Jobs")


def render_page(request, active_page, page_title):
    return render(
        request,
        "mro/mro_dashboard.html",
        {
            "active_page": active_page,
            "page_title": page_title,
        },
    )

@login_required
@user_passes_test(is_mro, login_url="login")
def convert_invoice_pdf(request, invoice_id):
    invoice = ClientInvoice.objects.get(id=invoice_id)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.setTitle("Client Invoice")

    pdf.drawString(50, 800, "CLIENT INVOICE DETAILS")
    pdf.line(50, 785, 550, 785)

    details = [
        ("Invoice ID", invoice.id),
        ("Client Name", invoice.client_name),
        ("Contact Number", invoice.contact_number),
        ("Gender", invoice.gender),
        ("Product Name", invoice.product_name),
        ("Serial Number", invoice.serial_number),
        ("Purchase Date", str(invoice.purchase_date)),
        ("Under Warranty", "Yes" if invoice.under_warranty else "No"),
        ("Installed", "Yes" if invoice.installed else "No"),
        ("Issue Reported", "Yes" if invoice.issue_reported else "No"),
        ("Proof of Purchase", "Yes" if invoice.proof_of_purchase else "No"),
        ("Created At", str(invoice.created_at)),
    ]

    y = 750

    for label, value in details:
        pdf.drawString(50, y, f"{label}: {value}")
        y -= 30

    pdf.save()

    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/pdf",
    )
    response["Content-Disposition"] = (
        f'attachment; filename="invoice_{invoice.id}.pdf"'
    )

    return response


@login_required
@user_passes_test(is_mro, login_url="login")
@require_POST
def send_invoice_to_tm(request, invoice_id):
    invoice = get_object_or_404(ClientInvoice, id=invoice_id)

    if invoice.workflow_status != "mro":
        messages.warning(request, "This invoice has already been sent to TM.")
    else:
        invoice.workflow_status = "waiting_tm"
        invoice.save(update_fields=["workflow_status"])
        messages.success(request, "Invoice sent to TM successfully!")

    return redirect("mro:invoice_register")