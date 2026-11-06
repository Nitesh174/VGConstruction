
from django.db import models


class ContactEnquiry(models.Model):
    SERVICE_CHOICES = [
        ("construction", "House Construction"),
        ("interior", "Interior Design"),
        ("renovation", "Renovation"),
        ("planning", "Architectural Planning"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    service = models.CharField(
        max_length=30,
        choices=SERVICE_CHOICES,
        default="other",
    )
    budget = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"

    class Meta:
        ordering = ["-created_at"]
