from clinic.models import Clinic
from user.models import Medic, TimeSlot
from user.models import Medic
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from user.models import User, Patient, Medic, TimeSlot

User = get_user_model()

class UserManagerTest(TestCase):

    def setUp(self):
        self.phone_number = '1234567890'
        self.password = 'testpassword'
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 30,
            'is_patient': True,
        }

    def test_create_user_with_valid_data(self):
        user = User.objects.create_user(
            phone_number=self.phone_number,
            password=self.password,
            **self.user_data
        )
        self.assertEqual(user.phone_number, self.phone_number)
        self.assertTrue(user.check_password(self.password))
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.age, 30)
        self.assertTrue(user.is_patient)
        self.assertFalse(user.is_medic)




class PatientModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='1234567890',
            first_name='John',
            last_name='Doe',
            age=30
        )
        self.patient = Patient.objects.create(
            user=self.user,
            address='123 Medical St',
            medical_history='No significant history',
            insurance_info='ABC Insurance',
            blood_group='O+',
            drug_allergy='None',
            special_medicine='None',
            systemic_diseases='None'
        )

    def test_patient_creation(self):
        patient = Patient.objects.get(user=self.user)
        self.assertEqual(patient.user.first_name, 'John')
        self.assertEqual(patient.address, '123 Medical St')
        self.assertEqual(str(patient), f'patient {self.user}')


class MedicModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='0987654321',
            first_name='Jane',
            last_name='Smith',
            age=35
        )
        self.medic = Medic.objects.create(
            user=self.user,
            specialization='Cardiologist',
            medical_system_number='MED12345',
            accepted=True
        )

    def test_medic_creation(self):
        medic = Medic.objects.get(user=self.user)
        self.assertEqual(medic.specialization, 'Cardiologist')
        self.assertEqual(medic.medical_system_number, 'MED12345')
        self.assertEqual(medic.accepted, True)
        self.assertEqual(str(medic), f'{self.user} Cardiologist specialize.')



class TimeSlotModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='1231231234',
            first_name='Dr. John',
            last_name='Doe',
            age=45
        )
        self.medic = Medic.objects.create(
            user=self.user,
            specialization='Dermatologist',
            medical_system_number='DERM56789',
            accepted=True
        )
        self.clinic = Clinic.objects.create(
            name='Health Clinic',
            address='456 Clinic Road'
        )
        self.timeslot = TimeSlot.objects.create(
            medic=self.medic,
            clinic=self.clinic,
            day_of_week=2,
            start_time='09:00:00',
            end_time='17:00:00',
            avg_visit_time=30,
            is_active=True
        )

    def test_timeslot_creation(self):
        timeslot = TimeSlot.objects.get(medic=self.medic, day_of_week=2)
        self.assertEqual(timeslot.day_of_week, 2)
        self.assertEqual(timeslot.start_time.strftime('%H:%M:%S'), '09:00:00')
        self.assertEqual(timeslot.end_time.strftime('%H:%M:%S'), '17:00:00')
        self.assertEqual(timeslot.avg_visit_time, 30)
        self.assertEqual(timeslot.is_active, True)
        self.assertEqual(
            str(timeslot), f"{self.medic} - 2 09:00:00 to 17:00:00 at {self.clinic.address}")

    def test_timeslot_unique_together(self):
        with self.assertRaises(Exception):
            TimeSlot.objects.create(
                medic=self.medic,
                clinic=self.clinic,
                day_of_week=2,
                start_time='08:00:00',
                end_time='12:00:00',
                avg_visit_time=30
            )
