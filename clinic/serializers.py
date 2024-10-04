from rest_framework import serializers

from .models import Clinic


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ['id', 'name', 'address', 'clinic_serial', 'image']

    def validate_clinic_serial(self, value):
        if Clinic.objects.filter(clinic_serial=value).exists():
            raise serializers.ValidationError('clinic serial must be unique')
        return value


class AdminClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ['id', 'name', 'address',
                  'clinic_serial', 'image', 'accepted']
