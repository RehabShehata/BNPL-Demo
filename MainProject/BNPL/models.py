from django.conf import settings
from django.db import models
from django.utils import timezone

from accounts.models import User

# Create your models here.
class Plan(models.Model):
    PLAN_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    merchant = models.ForeignKey(User, related_name="plans_created", on_delete=models.CASCADE)
    customer = models.ForeignKey(User, related_name="plans", on_delete=models.CASCADE)

    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    number_of_installments = models.PositiveIntegerField()
    start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=PLAN_STATUS_CHOICES, default='Pending')

    def __str__(self) -> str:
        return f"Plan #{self.pk} – {self.total_amount} × {self.number_of_installments}"

class Installment(models.Model):
    STATUS_CHOICES = (("Pending", "Pending"), ("Paid", "Paid"))

    plan = models.ForeignKey(
        Plan, related_name="installments", on_delete=models.CASCADE
    )
    installment_number = models.PositiveIntegerField()
    amount_due = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(
        max_length=7, choices=STATUS_CHOICES, default="Pending"
    )
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("plan", "installment_number")
        ordering = ("due_date",)

    def mark_paid(self):
        self.status = "Paid"
        self.paid_at = timezone.now()
        self.save()

    def __str__(self) -> str:
        return f"Instalment {self.installment_number} of Plan #{self.plan_id}"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_merchant = models.BooleanField(default=False)
