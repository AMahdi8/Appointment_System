from django.test import TestCase
from django.db.utils import IntegrityError
from user.models import Medic, Patient, User
from medical_records.models import MedicalRecord, Prescription


class MedicalRecordModelTest(TestCase):

    def setUp(self):
        self.medic = Medic.objects.create(user=User.objects.create(phone_number='786534', first_name='ali', last_name='mosavi',
                                          age=45, is_medic=True), specialization='hand', medical_system_number='32432', accepted=True)
        self.patient = Patient.objects.create(user=User.objects.create(phone_number='7864534', first_name='ahmad', last_name='keyvani',
                                                                       age=45, is_patient=True))
        self.prescription = Prescription.objects.create(
            prescription_number=123456,
            drugs='Drug A, Drug B'
        )

    def test_create_medical_record(self):
        medical_record = MedicalRecord.objects.create(
            medic=self.medic,
            patient=self.patient,
            prescription=self.prescription,
            illnes_subject='Flu',
            illness='Common cold with flu symptoms',
            hospitalized=False
        )

        self.assertEqual(MedicalRecord.objects.count(), 1)
        self.assertEqual(medical_record.illnes_subject, 'Flu')

    def test_unique_constraint(self):
        MedicalRecord.objects.create(
            medic=self.medic,
            patient=self.patient,
            illnes_subject='Flu',
            illness='Common cold with flu symptoms',
            hospitalized=False
        )

        with self.assertRaises(IntegrityError):
            MedicalRecord.objects.create(
                medic=self.medic,
                patient=self.patient,
                illnes_subject='Diabetes',
                illness='Chronic condition',
                hospitalized=False
            )

    def test_create_without_prescription(self):
        medical_record = MedicalRecord.objects.create(
            medic=self.medic,
            patient=self.patient,
            illnes_subject='Flu',
            illness='Common cold with flu symptoms',
            hospitalized=False
        )

        self.assertIsNone(medical_record.prescription)
        self.assertEqual(MedicalRecord.objects.count(), 1)

    def test_field_data(self):
        medical_record = MedicalRecord.objects.create(
            medic=self.medic,
            patient=self.patient,
            illnes_subject='Pneumonia',
            illness='Severe respiratory condition',
            hospitalized=True
        )

        self.assertEqual(medical_record.illnes_subject, 'Pneumonia')
        self.assertEqual(medical_record.illness,
                         'Severe respiratory condition')
        self.assertTrue(medical_record.hospitalized)

    def test_prescription_assignment(self):
        medical_record = MedicalRecord.objects.create(
            medic=self.medic,
            patient=self.patient,
            prescription=self.prescription,
            illnes_subject='Flu',
            illness='Mild flu symptoms',
            hospitalized=False
        )

        self.assertEqual(medical_record.prescription, self.prescription)
        self.assertEqual(
            medical_record.prescription.prescription_number, 123456)
