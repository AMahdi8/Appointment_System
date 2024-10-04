from math import ceil
from rest_framework import serializers

from appointment.models import Appointment
from clinic.serializers import ClinicSerializer

from .models import Medic, Patient, TimeSlot, User


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['phone_number', 'first_name', 'last_name', 'age']


class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp_code = serializers.CharField()


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ['user', 'address', 'medical_history', 'insurance_info', 'blood_group',
                  'drug_allergy', 'special_medicine', 'systemic_diseases']

    def __init__(self, *args, **kwargs):
        super(PatientSerializer, self).__init__(*args, **kwargs)

        optional_fields = ['address', 'medical_history', 'insurance_info',
                           'blood_group', 'drug_allergy', 'special_medicine', 'systemic_diseases']

        for field in optional_fields:
            self.fields[field].required = False

    def save(self, **kwargs):
        kwargs['user'] = self.context['request'].user
        return super().save(**kwargs)

    def create(self, validated_data):
        user = self.context['request'].user
        user.is_patient = True
        user.is_medic = False
        user.save()

        return super().create(validated_data)


class CreatePatientUserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    age = serializers.IntegerField()
    address = serializers.CharField()
    medical_history = serializers.CharField()
    insurance_info = serializers.CharField()
    drug_allergy = serializers.CharField()
    blood_group = serializers.CharField()
    special_medicine = serializers.CharField()
    systemic_diseases = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super(CreatePatientUserSerializer, self).__init__(*args, **kwargs)

        optional_fields = ['address', 'medical_history', 'insurance_info',
                           'blood_group', 'drug_allergy', 'special_medicine', 'systemic_diseases']

        for field in optional_fields:
            self.fields[field].required = False

    def save(self, **kwargs):
        kwargs['user'] = self.context['request'].user
        return super().save(**kwargs)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class UpdatePatientUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    age = serializers.IntegerField(source='user.age')

    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'age', 'address', 'medical_history', 'insurance_info',
                  'blood_group', 'drug_allergy', 'special_medicine', 'systemic_diseases']

    def __init__(self, *args, **kwargs):
        super(UpdatePatientUserSerializer, self).__init__(*args, **kwargs)

        optional_fields = ['first_name', 'last_name', 'age', 'address', 'medical_history', 'insurance_info',
                           'blood_group', 'drug_allergy', 'special_medicine', 'systemic_diseases']

        for field in optional_fields:
            self.fields[field].required = False

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        first_name = user_data.get('first_name', None)
        last_name = user_data.get('last_name', None)
        age = user_data.get('age', None)

        if first_name:
            instance.user.first_name = first_name
        if last_name:
            instance.user.last_name = last_name
        if age:
            instance.user.age = age

        instance.user.save()

        instance.address = validated_data.get('address', instance.address)
        instance.medical_history = validated_data.get(
            'medical_history', instance.medical_history)
        instance.insurance_info = validated_data.get(
            'insurance_info', instance.insurance_info)
        instance.blood_group = validated_data.get(
            'blood_group', instance.blood_group)
        instance.drug_allergy = validated_data.get(
            'drug_allergy', instance.drug_allergy)
        instance.special_medicine = validated_data.get(
            'special_medicine', instance.special_medicine)
        instance.systemic_diseases = validated_data.get(
            'systemic_diseases', instance.systemic_diseases)

        instance.save()

        return instance


class MedicSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Medic
        fields = ['user', 'image', 'specialization', 'medical_system_number']

    def save(self, **kwargs):
        kwargs['user'] = self.context['request'].user
        return super().save(**kwargs)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CreateMedicUserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    age = serializers.IntegerField()
    specialization = serializers.CharField()
    medical_system_number = serializers.CharField()
    image = serializers.ImageField(required=False)

    def save(self, **kwargs):
        kwargs['user'] = self.context['request'].user
        return super().save(**kwargs)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class UpdateMedicUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source='user.first_name', required=False)
    last_name = serializers.CharField(
        source='user.last_name', required=False)
    age = serializers.IntegerField(
        source='user.age', required=False)
    specialization = serializers.CharField(required=False)
    medical_system_number = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Medic
        fields = ['first_name', 'last_name', 'age',
                  'image', 'specialization', 'medical_system_number']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')
        age = user_data.get('age')

        instance.specialization = validated_data.get(
            'specialization', instance.specialization)
        instance.medical_system_number = validated_data.get(
            'medical_system_number', instance.medical_system_number)
        instance.image = validated_data.get('image', instance.image)

        instance.save()

        if first_name:
            instance.user.first_name = first_name
        if last_name:
            instance.user.last_name = last_name
        if age:
            instance.user.age = age

        if not instance.user.first_name or not instance.user.last_name or not instance.user.age:
            raise serializers.ValidationError(
                'first_name and last_name and age can not be blank')
        instance.user.save()

        return instance


class CREATEMedicAvailableTimeSerializer(serializers.ModelSerializer):
    medic = MedicSerializer(read_only=True)

    class Meta:
        model = TimeSlot
        fields = ['medic', 'clinic', 'day_of_week',
                  'start_time', 'end_time', 'avg_visit_time']

    def create(self, validated_data):
        user = self.context['request'].user

        if not hasattr(user, 'medic'):
            raise serializers.ValidationError(
                'User must be a medic to create a time slot.')

        if TimeSlot.objects.filter(medic=user.medic, day_of_week=validated_data['day_of_week']).exists():
            raise serializers.ValidationError(
                "You can't set a day of week twice."
            )

        medic = user.medic
        clinic = validated_data['clinic']
        start_time = validated_data['start_time']
        end_time = validated_data['end_time']
        avg_visit_time = validated_data['avg_visit_time']

        if not medic.accepted:
            raise serializers.ValidationError('Medic must be accepted first.')

        if not clinic.accepted:
            raise serializers.ValidationError('Clinic must be accepted first.')

        total_time = abs(ceil(end_time.hour - start_time.hour))

        avg_patient_visit = ceil(total_time // (avg_visit_time / 60))

        validated_data['medic'] = medic
        validated_data['avg_patient_visit'] = avg_patient_visit

        return super().create(validated_data)


class UPDATEMedicAvailableTimeSerializer(serializers.ModelSerializer):
    medic = MedicSerializer(read_only=True)

    class Meta:
        model = TimeSlot
        fields = ['medic', 'clinic', 'day_of_week',
                  'start_time', 'end_time', 'avg_visit_time', 'avg_patient_visit', 'is_active']


class GETMedicAvailableTimeSerializer(serializers.ModelSerializer):
    medic = MedicSerializer(read_only=True)
    clinic = ClinicSerializer(read_only=True)

    class Meta:
        model = TimeSlot
        fields = ['id', 'medic', 'clinic', 'day_of_week',
                  'start_time', 'end_time', 'avg_visit_time', 'avg_patient_visit', 'is_active']


class MedicOrPatientSerializers(serializers.Serializer):
    phone_number = serializers.CharField(source='user.phone_number')
    id = serializers.IntegerField()
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    age = serializers.IntegerField(source='user.age')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if isinstance(instance, Medic):
            representation['role'] = 'medic'
        elif isinstance(instance, Patient):
            representation['role'] = 'patient'
        return representation
