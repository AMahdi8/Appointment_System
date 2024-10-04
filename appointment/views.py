from datetime import datetime, timedelta
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import Response, status
from rest_framework.decorators import action

from .models import Appointment, Prescription
from .serializers import AppointmentSerializer, PrescriptionSerializer, RetrieveAppointmentSerializer, UpdateAppointmentSerializer

from user.permissions import IsMedicOrAdmin, IsPatientOrAdmin, IsAppointmentRelated


class AppointmentViewSet(ModelViewSet):
    serializer_class = AppointmentSerializer

    def get_serializer_class(self):
        if self.action == 'update':
            return UpdateAppointmentSerializer

        elif self.action == 'retrieve':
            return RetrieveAppointmentSerializer

        return AppointmentSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return Appointment.objects.all()

        if user.is_medic:
            return Appointment.objects.filter(time__medic=user.medic)

        elif user.is_patient:
            return Appointment.objects.filter(patient=user.patient)

        return Appointment.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            return [IsPatientOrAdmin()]

        elif self.action == 'update':
            return [IsMedicOrAdmin()]

        return [IsAuthenticated()]

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated], url_path='my_appointment')
    def my_appointment(self, request):
        user = self.request.user

        appointments = Appointment.objects.none()
        now = datetime.now()

        if user.is_medic:
            appointments = Appointment.objects.filter(
                Q(time__medic=user.medic) &
                Q(appointment_datetime__gt=now) &
                Q(appointment_datetime__lt=now+timedelta(days=7)))\
                .order_by('appointment_datetime')

        elif user.is_patient:
            appointments = Appointment.objects.filter(
                Q(patient=user.patient) &
                Q(appointment_datetime__gt=now) &
                Q(appointment_datetime__lt=now+timedelta(days=7)))\
                .order_by('appointment_datetime')

        serializer = RetrieveAppointmentSerializer(appointments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PrescriptionViewSet(ModelViewSet):
    serializer_class = PrescriptionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Prescription.objects.all()

        patient = getattr(user, 'patient', None)
        medic = getattr(user, 'medic', None)

        if medic and user.is_medic:
            return Prescription.objects.filter(appointment__time__medic=medic)

        if patient and user.is_patient:
            return Prescription.objects.filter(appointment__patient=patient)

        return Prescription.objects.none()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]

        elif self.request.method == 'DELETE':
            return [IsAdminUser()]

        return [IsMedicOrAdmin()]
