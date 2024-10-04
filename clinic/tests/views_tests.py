from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from clinic.models import Clinic
from user.models import Medic

User = get_user_model()


class ClinicViewSetTests(APITestCase):

    def setUp(self):
        self.patient_user = User.objects.create_user(
            phone_number='954260897',
            is_patient=True,
            is_medic=False,
            first_name='mohammad',
            last_name='mohammady',
            age=64
        )

        self.medic_user = User.objects.create_user(
            phone_number='986352',
            is_medic=True,
            is_patient=False,
            first_name='mahdi',
            last_name='siadati',
            age=23
        )

        self.medic = Medic.objects.create(
            user=self.medic_user,
            specialization='hand',
            medical_system_number='1234',
            accepted=True
        )

        self.admin_user = User.objects.create_superuser(
            phone_number='435252',
            password='523',
        )

        self.clinic = Clinic.objects.create(
            name="Test Clinic",
            address="123 Test Address",
            clinic_serial="CLINIC001",
            accepted=True
        )

        self.clinic_list_url = reverse('clinic-list')
        self.clinic_detail_url = reverse(
            'clinic-detail', args=[self.clinic.id])

    def test_get_clinics_authenticated(self):
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.get(self.clinic_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_clinics_unauthenticated(self):
        response = self.client.get(self.clinic_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_clinic_as_medic(self):
        self.client.force_authenticate(user=self.medic_user)
        data = {
            'name': 'New Clinic',
            'address': '456 New Street',
            'clinic_serial': 'CLINIC002'
        }
        response = self.client.post(self.clinic_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Clinic.objects.count(), 2)

    def test_post_clinic_as_patient(self):
        self.client.force_authenticate(user=self.patient_user)
        data = {
            'name': 'New Clinic',
            'address': '456 New Street',
            'clinic_serial': 'CLINIC002'
        }
        response = self.client.post(self.clinic_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_clinic_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.clinic_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Clinic.objects.count(), 0)

    def test_delete_clinic_as_medic(self):
        self.client.force_authenticate(user=self.medic_user)
        response = self.client.delete(self.clinic_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_clinic_as_medic(self):
        self.client.force_authenticate(user=self.medic_user)
        data = {'name': 'Partially Updated Clinic'}
        response = self.client.patch(
            self.clinic_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.clinic.refresh_from_db()
        self.assertEqual(self.clinic.name, 'Partially Updated Clinic')
