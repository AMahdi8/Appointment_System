from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import Response, status
from rest_framework.exceptions import ValidationError

from user.permissions import IsMedicOrAdmin, IsPatientOrAdmin

from .models import MedicalRecord
from .serializers import GETMedicalRecordSerializer, POSTMedicalRecordSerializer


class MedicalRecordViewSet(ModelViewSet):
    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return MedicalRecord.objects.all()

        if user.is_medic:
            return MedicalRecord.objects.filter(medic=user.medic)

        elif user.is_patient:
            return MedicalRecord.objects.filter(patient=user.patient)

        return MedicalRecord.objects.none()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GETMedicalRecordSerializer

        return POSTMedicalRecordSerializer

    def get_permissions(self):

        if self.request.method == 'GET':
            return [IsAuthenticated()]

        elif self.request.method in ['PATCH', 'PUT', 'POST']:
            return [IsMedicOrAdmin()]

        return [IsAdminUser()]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(medic=user.medic)
