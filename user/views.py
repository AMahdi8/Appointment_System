import random
from datetime import datetime, timedelta, time as datetime_time

from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import Response, status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError

from appointment.models import Appointment
from user.permissions import IsMedicOrAdmin, IsOwnerOrAdmin

from .utils import increment_failed_attemps_otp, is_blocked, send_sms
from .serializers import CREATEMedicAvailableTimeSerializer, CreateMedicUserSerializer, CreatePatientUserSerializer, GETMedicAvailableTimeSerializer, MedicOrPatientSerializers, UpdateMedicUserSerializer, PatientSerializer, UpdatePatientUserSerializer, SendOTPSerializer, UPDATEMedicAvailableTimeSerializer, UserSerializer, VerifyOTPSerializer, MedicSerializer
from .models import Medic, Patient, TimeSlot, User


class UserViewSet(ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny], url_path='send_otp')
    def send_otp(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']

        otp_code = random.randint(100000, 999999)
        print(otp_code)

        # send SMS function
        send_sms(phone_number)
        
        old_otp = cache.get(phone_number)
        if old_otp:
            return Response(f"You already receive otp code. Please try again later",
                            status=status.HTTP_403_FORBIDDEN)

        cache.set(phone_number, str(otp_code),
                  timeout=120)  # ttl 2 minwute

        return Response('OTP sent successfully.', status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET', 'POST'], permission_classes=[AllowAny], url_path='verify_otp')
    def verify_otp(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        otp_code = serializer.validated_data['otp_code']

        if is_blocked(phone_number):
            return Response('Too many failed attempts. Please try again later.', status=status.HTTP_403_FORBIDDEN)

        stored_otp = cache.get(phone_number)
        if stored_otp and stored_otp == otp_code:

            cache.delete(phone_number)
            cache.delete(f'failed_attempts_{phone_number}')

            user, created = User.objects.get_or_create(
                phone_number=phone_number)

            refresh = RefreshToken.for_user(user)

            if created:
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_201_CREATED)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_202_ACCEPTED)

        increment_failed_attemps_otp(phone_number)
        return Response('Please enter a valid code')

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated], url_path='medic_or_patient')
    def medic_or_patient(self, request):
        user = request.user
        medic = getattr(user, 'medic', None)
        patient = getattr(user, 'patient', None)

        data = {
            'patient': None,
            'medic': None
        }

        if patient:
            data['patient'] = MedicOrPatientSerializers(patient).data
        if medic:
            data['medic'] = MedicOrPatientSerializers(medic).data

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated], url_path='medic_entry')
    def medic_entry(self, request):
        user = request.user
        medic = getattr(user, 'medic', None)

        if medic:
            user.is_medic = True
            user.is_patient = False
            user.save()
            return Response('You logged in as medic.', status=status.HTTP_202_ACCEPTED)

        return Response("You can't log in as medic", status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated], url_path='patient_entry')
    def patient_entry(self, request):
        user = request.user
        patient = getattr(user, 'patient', None)

        if patient:
            user.is_medic = False
            user.is_patient = True
            user.save()
            return Response('You logged in as Patient.', status=status.HTTP_202_ACCEPTED)

        return Response("You can't log in as Patient", status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['GET', 'PUT', 'PATCH', 'DELETE'], permission_classes=[IsAuthenticated], url_path='me')
    def me(self, request):
        user = self.request.user
        if self.request.method == 'GET':
            if user.is_medic:
                me = Medic.objects.get(user=user)
                serializer = MedicSerializer(me)

            elif user.is_patient:
                me = Patient.objects.get(user=user)
                serializer = PatientSerializer(me)

            else:
                me = User.objects.get(id=user.id)
                serializer = UserSerializer(me)

        elif self.request.method in ['PUT', 'PATCH']:
            if user.is_medic:
                me = Medic.objects.get(user=user)
                serializer = UpdateMedicUserSerializer(
                    me, data=request.data, context={'request': request})
                serializer.is_valid(raise_exception=True)
                serializer.save()

            elif user.is_patient:
                me = Patient.objects.get(user=user)
                serializer = UpdatePatientUserSerializer(
                    me, data=request.data, context={'request': request})
                serializer.is_valid(raise_exception=True)
                serializer.save()

            else:
                me = user
                serializer = UserSerializer(instance=me, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

        elif self.request.method == 'DELETE':
            user.delete()
            return Response('You deleted your account.', status=status.HTTP_202_ACCEPTED)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientViewSet(ListModelMixin,
                     CreateModelMixin,
                     DestroyModelMixin,
                     GenericViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        user = self.request.user
        user.is_patient = False
        user.save()
        return super().perform_destroy(instance)

    def get_permissions(self):
        if self.action == 'list':
            return [IsAdminUser()]
        elif self.action == 'destroy':
            return [IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        user = self.request.user

        if Patient.objects.filter(user=request.user).exists():
            raise ValidationError(
                'A patient profile already exists for this user.')

        if user.first_name:
            serializer = PatientSerializer(
                data=request.data, context={'request': request})
        else:
            serializer = CreatePatientUserSerializer(
                data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)

        if not user.first_name:
            user.first_name = serializer.validated_data.get('first_name')
            user.last_name = serializer.validated_data.get('last_name')
            user.age = serializer.validated_data.get('age')
        user.is_medic = False
        user.is_patient = True
        user.save()

        Patient.objects.create(
            user=user,
            address=serializer.validated_data.get('address', None),
            medical_history=serializer.validated_data.get(
                'medical_history', None),
            insurance_info=serializer.validated_data.get(
                'insurance_info', None),
            drug_allergy=serializer.validated_data.get('drug_allergy', None),
            blood_group=serializer.validated_data.get('blood_group', None),
            special_medicine=serializer.validated_data.get(
                'special_medicine', None),
            systemic_diseases=serializer.validated_data.get(
                'systemic_diseases', None),
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MedicViewSet(ListModelMixin,
                   RetrieveModelMixin,
                   CreateModelMixin,
                   DestroyModelMixin,
                   GenericViewSet):

    serializer_class = MedicSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return Medic.objects.all()

        return Medic.objects.filter(accepted=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        user = self.request.user
        user.is_medic = False
        user.save()
        return super().perform_destroy(instance)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'DELETE':
            return [IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        user = self.request.user

        if user.first_name:
            serializer = MedicSerializer(
                data=request.data, context={'request': request})
        else:
            serializer = CreateMedicUserSerializer(
                data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)

        if not user.first_name:
            user.first_name = serializer.validated_data.get('first_name')
            user.last_name = serializer.validated_data.get('last_name')
            user.age = serializer.validated_data.get('age')
        user.is_medic = True
        user.is_patient = False
        user.save()

        specialization = serializer.validated_data.get('specialization')
        medical_system_number = serializer.validated_data.get(
            'medical_system_number')
        image = serializer.validated_data.get('image')

        Medic.objects.create(user=user,
                             specialization=specialization,
                             medical_system_number=medical_system_number,
                             image=image
                             )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['GET'], permission_classes=[AllowAny], url_path='appointment_times')
    def appointment_times(slef, request, pk):
        medic = get_object_or_404(Medic, id=pk)
        times = TimeSlot.objects.filter(medic=medic, is_active=True)
        availvable_times = []
        days_of_week = []
        for time in times:
            days_of_week.append(time.day_of_week)

        today = datetime.now()
        for day_of_week in days_of_week:
            day_difference = day_of_week - today.weekday()
            if day_difference <= 0:
                day_difference += 7

            time_zero = datetime_time()
            day = datetime.combine(today.date(), time_zero)

            appointmented_count = Appointment.objects.filter(
                Q(appointment_datetime__gt=day+timedelta(days=day_difference)) &
                Q(appointment_datetime__lt=day+timedelta(days=day_difference+1)))\
                .count()

            weekday_appointment = times.get(day_of_week=day_of_week)
            if appointmented_count < weekday_appointment.avg_patient_visit:
                availvable_times.append(weekday_appointment)

        serializer = GETMedicAvailableTimeSerializer(
            availvable_times, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MedicAvailableTimeViewSet(ModelViewSet):
    permission_classes = [IsMedicOrAdmin]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return CREATEMedicAvailableTimeSerializer
        elif self.request.method in ['PUT', 'PATCH']:
            return UPDATEMedicAvailableTimeSerializer
        return GETMedicAvailableTimeSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return TimeSlot.objects.all()

        user = User.objects.get(id=user.id)
        medic = Medic.objects.select_related('user').get(user=user)
        times = TimeSlot.objects.select_related('medic').filter(medic=medic)
        return times

    def perform_create(self, serializer):
        serializer.save(medic=self.request.user.medic)

    def perform_update(self, serializer):
        serializer.save(medic=self.request.user.medic)
