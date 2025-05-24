from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Installment, Plan

@receiver(post_save, sender=Installment)
def update_plan_status(sender, instance, **kwargs):
    plan = instance.plan
    # Check if all installments are paid
    if plan.installments.filter(status='Pending').exists():
        # Still have pending installments
        if plan.status != 'Pending':
            plan.status = 'Pending'
            plan.save(update_fields=['status'])
    else:
        # All installments are paid
        if plan.status != 'Completed':
            plan.status = 'Completed'
            plan.save(update_fields=['status'])
