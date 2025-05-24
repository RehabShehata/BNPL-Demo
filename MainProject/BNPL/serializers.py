from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP
from rest_framework import serializers

from accounts.models import User
from .models import Plan, Installment

class InstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installment
        fields = (
            "id",
            "installment_number",
            "amount_due",
            "due_date",
            "status",
            "paid_at",
        )

class PlanSerializer(serializers.ModelSerializer):
    installments = InstallmentSerializer(many=True, read_only=True)

    class Meta:
        model = Plan
        fields = (
            "id",
            "merchant",
            "customer",
            "total_amount",
            "number_of_installments",
            "start_date",
            "created_at",
            "installments",
            "status"
        )
        read_only_fields = ("merchant", "created_at", "installments")

class PlanCreateSerializer(serializers.Serializer):
    """
    Accepts merchant-side payload and auto-creates Installment rows.
    """

    # input fields
    customer_email = serializers.EmailField(write_only=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    number_of_installments = serializers.IntegerField(min_value=1)
    start_date = serializers.DateField()

    # output (after create)
    plan = PlanSerializer(read_only=True)

    def validate_customer_email(self, value):
       try:
         return User.objects.get(email=value)
       except User.DoesNotExist:
         raise serializers.ValidationError("No user with that email")
    
    def create(self, validated):
        merchant = self.context["request"].user
        customer = validated["customer_email"]  # replaced with User instance
        total = validated["total_amount"].quantize(Decimal("0.01"), ROUND_HALF_UP)
        n = validated["number_of_installments"]
        start_date = validated["start_date"]

        # 1. Create the plan record
        plan = Plan.objects.create(
            merchant=merchant,
            customer=customer,
            total_amount=total,
            number_of_installments=n,
            start_date=start_date,
        )

        # 2. Calculate equal installments (first one adjusted for rounding)
        base = (total / n).quantize(Decimal("0.01"), ROUND_HALF_UP)
        amounts = [base] * n
        amounts[0] += total - sum(amounts)  # add rounding diff to first

        inst_objs = []
        for idx, amount in enumerate(amounts, start=1):
            due = start_date + timedelta(days=30 * (idx - 1))
            inst_objs.append(
                Installment(
                    plan=plan,
                    installment_number=idx,
                    amount_due=amount,
                    due_date=due,
                )
            )
        Installment.objects.bulk_create(inst_objs)
        return plan
