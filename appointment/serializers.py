from datetime import timedelta, datetime
from rest_framework import serializers

from medical_records.models import MedicalRecord
from medical_records.serializers import GETMedicalRecordSerializer
from user.serializers import GETMedicAvailableTimeSerializer, PatientSerializer

from .models import Appointment, Prescription


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['id', 'prescription_number', 'drugs']


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    appointment_datetime = serializers.DateTimeField(read_only=True)
    appointment_number = serializers.IntegerField(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'time', 'short_description',
                  'appointment_datetime', 'appointment_number']

    def create(self, validated_data):
        user = self.context['request'].user
        today = datetime.now()

        time = validated_data['time']

        if not time.is_active:
            raise serializers.ValidationError(
                'No Medic appointment time matches.'
            )

        time_day = time.day_of_week
        day_difference = time_day - today.weekday()
        if day_difference <= 0:
            day_difference += 7

        appointment_date = today + timedelta(days=day_difference)

        appointment_reserved = Appointment.objects.filter(
            appointment_datetime__date=appointment_date.date(), time=time
        )

        appointment_reserved_count = appointment_reserved.count()

        if time.avg_patient_visit <= appointment_reserved_count:
            raise serializers.ValidationError(
                'You cannot reserve this appointment; it is fully booked.')

        appointment_number = appointment_reserved_count + 1

        start_time = datetime.combine(appointment_date.date(), time.start_time)

        appointment_datetime = start_time + \
            timedelta(minutes=appointment_reserved_count * time.avg_visit_time)

        if Appointment.objects.filter(time=time).\
                filter(appointment_datetime__gte=appointment_datetime).\
                filter(appointment_datetime__lte=appointment_datetime+timedelta(minutes=time.avg_visit_time)).\
                count():
            raise serializers.ValidationError(
                'You already have another appointment for this time.'
            )

        validated_data['appointment_datetime'] = appointment_datetime
        validated_data['appointment_number'] = appointment_number
        validated_data['patient'] = user.patient

        medical_record, created = MedicalRecord.objects.get_or_create(
            medic=time.medic, patient=user.patient)
        prescription = Prescription.objects.create()

        validated_data['medical_record'] = medical_record
        validated_data['prescription'] = prescription

        return super().create(validated_data)

    def save(self, **kwargs):
        kwargs['patient'] = self.context['request'].user.patient
        return super().save(**kwargs)


class RetrieveAppointmentSerializer(serializers.ModelSerializer):
    prescription = PrescriptionSerializer()
    medical_record = GETMedicalRecordSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'prescription', 'medical_record', 'patient', 'time',
                  'short_description', 'appointment_datetime', 'appointment_number']


class UpdateAppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'time', 'short_description',
                  'appointment_datetime', 'appointment_number']
