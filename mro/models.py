
from django.db import models


class ClientInvoice(models.Model):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
        ("Prefer not to say", "Prefer not to say"),
    ]

    STATUS_CHOICES = [
        ("mro", "With MRO"),
        ("waiting_tm", "Waiting for TM Review"),
        ("completed_tm", "Completed by TM"),
        ("waiting_engineer", "Waiting for Engineer"),
        ("completed_engineer", "Completed by Engineer"),
        ("waiting_head", "Waiting for Head"),
        ("completed", "Completed"),
    ]

    client_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    product_name = models.CharField(max_length=150)
    serial_number = models.CharField(max_length=100)
    purchase_date = models.DateField()

    under_warranty = models.BooleanField()
    installed = models.BooleanField()
    issue_reported = models.BooleanField()
    proof_of_purchase = models.BooleanField()

    workflow_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="mro",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client_name
