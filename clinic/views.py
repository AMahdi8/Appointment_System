from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny

from .models import Clinic
from .serializers import AdminClinicSerializer, ClinicSerializer
from user.permissions import IsMedicOrAdmin


class ClinicViewSet(ModelViewSet):
    serializer_class = ClinicSerializer

    def get_serializer_class(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return AdminClinicSerializer

        return ClinicSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return Clinic.objects.all().order_by('clinic_serial')

        return Clinic.objects.filter(accepted=True).order_by('clinic_serial')

    def get_permissions(self):

        if self.request.method == 'GET':
            return [AllowAny()]

        elif self.request.method == 'POST':
            return [IsMedicOrAdmin()]

        return [IsAdminUser()]
