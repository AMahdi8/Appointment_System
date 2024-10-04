from rest_framework import serializers

from user.serializers import MedicSerializer, PatientSerializer

from .models import MedicalRecord


class POSTMedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'illnes_subject', 'illness', 'hospitalized']

    def create(self, validated_data):
        validated_data['medic'] = self.context['request'].user.medic
        return super().create(validated_data)

    def save(self, **kwargs):
        kwargs['medic'] = self.context['request'].user.medic
        return super().save(**kwargs)


class GETMedicalRecordSerializer(serializers.ModelSerializer):
    medic = MedicSerializer(read_only=True)
    patient = PatientSerializer()

    class Meta:
        model = MedicalRecord
        fields = ['medic', 'patient', 'illnes_subject',
                  'illness', 'hospitalized']
