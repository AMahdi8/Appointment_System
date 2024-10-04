from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from django.core.cache import cache
from rest_framework.test import APITestCase, APIClient

from clinic.models import Clinic
from user.models import Medic, Patient, TimeSlot

User = get_user_model()


class UserViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            phone_number='1234567890',
            first_name='mahdi',
            last_name='aleboyeh',
            age='22'
        )

        self.user_medic = User.objects.create_user(
            phone_number='0987654321',
            is_medic=True,
            first_name='reza',
            last_name='molaei',
            age='53'
        )

        self.user_patient = User.objects.create_user(
            phone_number='1122334455',
            is_patient=True,
            first_name='karim',
            last_name='shivaey',
            age='26'
        )

        self.patient = Patient.objects.create(
            user=self.user_patient
        )

        self.medic = Medic.objects.create(
            user=self.user_medic,
            specialization='hand',
            medical_system_number='245233',
            accepted=True
        )

    def test_send_otp(self):
        url = reverse('user-send-otp')
        response = self.client.post(url, {'phone_number': '1234567890'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('OTP sent successfully.', response.data)
        self.assertTrue(cache.get('1234567890'))

    def test_verify_otp(self):
        otp_code = '123456'
        cache.set('1234567890', otp_code, timeout=120)

        url = reverse('user-verify-otp')
        response = self.client.post(url, {
            'phone_number': '1234567890',
            'otp_code': otp_code
        })

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_medic_or_patient(self):
        self.client.force_authenticate(user=self.user_medic)
        url = reverse('user-medic-or-patient')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['medic'])
        self.assertIsNone(response.data['patient'])

        self.client.force_authenticate(user=self.user_patient)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['patient'])
        self.assertIsNone(response.data['medic'])

    def test_medic_entry(self):
        self.client.force_authenticate(user=self.user_medic)
        url = reverse('user-medic-entry')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.user_medic.refresh_from_db()
        self.assertTrue(self.user_medic.is_medic)

    def test_patient_entry(self):
        self.client.force_authenticate(user=self.user_patient)
        url = reverse('user-patient-entry')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.user_patient.refresh_from_db()
        self.assertTrue(self.user_patient.is_patient)

    def test_me_get_medic(self):
        self.client.force_authenticate(user=self.user_medic)
        url = reverse('user-me')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('specialization', response.data)

    def test_me_get_patient(self):
        self.client.force_authenticate(user=self.user_patient)
        url = reverse('user-me')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('medical_history', response.data)


    def test_me_put_medic(self):
        self.client.force_authenticate(user=self.user_medic)

        url = reverse('user-me')
        data = {
            'specialization': 'Neurology',
            'medical_system_number': '67890',
            'accepted': True
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.medic.refresh_from_db()
        self.assertEqual(self.medic.specialization, 'Neurology')
        self.assertEqual(self.medic.medical_system_number, '67890')

    def test_me_put_patient(self):
        self.client.force_authenticate(user=self.user_patient)

        url = reverse('user-me')
        data = {
            'address': '5678 Oak St',
            'medical_history': 'Previous surgery',
            'insurance_info': 'XYZ Insurance'
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.address, '5678 Oak St')
        self.assertEqual(self.patient.medical_history, 'Previous surgery')
        self.assertEqual(self.patient.insurance_info, 'XYZ Insurance')

    def test_me_patch_medic(self):
        self.client.force_authenticate(user=self.user_medic)

        url = reverse('user-me')
        data = {
            'specialization': 'Dermatology'
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.medic.refresh_from_db()
        self.assertEqual(self.medic.specialization, 'Dermatology')

    def test_me_patch_patient(self):
        self.client.force_authenticate(user=self.user_patient)

        url = reverse('user-me')
        data = {
            'medical_history': 'Asthma'
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.medical_history, 'Asthma')


class PatientViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            phone_number='09123456388', password='34')
        self.patient_user = User.objects.create_user(
            phone_number='09124456785', first_name='ali', last_name='riahy', age=42)
        self.patient_user_2 = User.objects.create_user(
            phone_number='09124436785', first_name='amir', last_name='siahy', age=53)
        self.patient = Patient.objects.create(user=self.patient_user_2)

    def test_list_patients_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('patient-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_patient(self):
        self.client.force_authenticate(user=self.patient_user)
        url = reverse('patient-list')
        data = {
            'address': '1234 Elm St',
            'medical_history': 'No known issues',
            'insurance_info': 'ABC Insurance'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_destroy_patient_as_owner(self):
        self.client.force_authenticate(user=self.patient_user_2)
        url = reverse('patient-detail', kwargs={'pk': self.patient.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_patient_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('patient-detail', kwargs={'pk': self.patient.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class MedicViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            phone_number='08948371845', password='52')
        self.medic_user = User.objects.create_user(
            phone_number='08944371845', first_name='abbas', last_name='shahian', age=33)
        self.medic_user_2 = User.objects.create_user(
            phone_number='08984371845', first_name='sina', last_name='ahmadi', age=37)
        self.medic = Medic.objects.create(
            user=self.medic_user_2, specialization='leg', medical_system_number='12345')

    def test_list_medics(self):
        url = reverse('medic-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_medic(self):
        self.client.force_authenticate(user=self.medic_user)
        url = reverse('medic-list')
        data = {
            'specialization': 'Neurology',
            'medical_system_number': '67890'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_medic(self):
        url = reverse('medic-detail', kwargs={'pk': self.medic.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy_medic_as_owner(self):
        self.client.force_authenticate(user=self.medic_user_2)
        url = reverse('medic-detail', kwargs={'pk': self.medic.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_medic_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('medic-detail', kwargs={'pk': self.medic.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class MedicAvailableTimeViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            phone_number='08948371845', password='52')
        self.medic_user = User.objects.create_user(
            phone_number='08944371845', first_name='abbas', last_name='shahian', age=33, is_medic=True)
        self.medic_user_2 = User.objects.create_user(
            phone_number='08984371845', first_name='sina', last_name='ahmadi', age=37, is_medic=True)
        self.medic = Medic.objects.create(
            user=self.medic_user, specialization='backache', medical_system_number='12345', accepted=True)
        self.clinic = Clinic.objects.create(
            name='ali', clinic_serial='532', accepted=True)
        self.timeslot = TimeSlot.objects.create(
            medic=self.medic, clinic=self.clinic, day_of_week=0, start_time='09:00:00', end_time='17:00:00', avg_visit_time=10)

    def test_list_available_times_as_medic(self):
        self.client.force_authenticate(user=self.medic_user)
        url = reverse('availabe_times-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_available_times_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('availabe_times-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_available_time(self):
        self.client.force_authenticate(user=self.medic_user)
        url = reverse('availabe_times-list')
        data = {
            'medic': self.medic.id,
            'clinic': self.clinic.id,
            'day_of_week': 1,
            'start_time': '10:00:00',
            'end_time': '15:00:00',
            'avg_visit_time': 30,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_destroy_available_time_as_medic(self):
        self.client.force_authenticate(user=self.medic_user)
        url = reverse('availabe_times-detail',
                      kwargs={'pk': self.timeslot.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_available_time_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('availabe_times-detail',
                      kwargs={'pk': self.timeslot.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
