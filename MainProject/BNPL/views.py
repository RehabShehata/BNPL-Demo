from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Plan, Installment
from .serializers import (
    PlanSerializer,
    PlanCreateSerializer,
    InstallmentSerializer,
)


class PlanViewSet(viewsets.ModelViewSet):
    """
    • POST /api/plans/  (merchant only)
    • GET  /api/plans/  (merchant → their plans, customer → their own)
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "is_merchant", False):  # define this flag in your user/profile
            return Plan.objects.filter(merchant=user)
        return Plan.objects.filter(customer=user)

    def get_serializer_class(self):
        if self.action == "create":
            return PlanCreateSerializer
        return PlanSerializer

    def perform_create(self, serializer):
        plan = serializer.save()
        # Wrap in read serializer for response
        read_ser = PlanSerializer(plan, context=self.get_serializer_context())
        self._response_data = read_ser.data  # stash for response

    def create(self, request, *args, **kwargs):
        if not request.user.is_merchant:
          return Response(
            {"detail": "Only merchants may create plans"},
           status=status.HTTP_403_FORBIDDEN,
            )
        super().create(request, *args, **kwargs)
        return Response(self._response_data, status=status.HTTP_201_CREATED)


class InstallmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only list/retrieve + custom pay action.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = InstallmentSerializer

    def get_queryset(self):
        user = self.request.user
        # merchants see installments under their plans; customer sees theirs
        return Installment.objects.filter(
            plan__merchant=user
        ) | Installment.objects.filter(plan__customer=user)

    # POST /api/installments/{id}/pay/
    @action(methods=["post"], detail=True, url_path="pay")
    def pay(self, request, pk=None):
        inst: Installment = self.get_object()

        # Only the customer of that plan may pay
        if inst.plan.customer != request.user:
            return Response(
                {"detail": "Only the plan customer can mark this as paid"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if inst.status == "Paid":
            return Response(
                {"detail": "Installment already paid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        inst.mark_paid()
        return Response(self.get_serializer(inst).data, status=status.HTTP_200_OK)
