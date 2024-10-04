from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError
from django.test import TestCase
from clinic.models import Clinic


class ClinicModelTest(TestCase):

    def setUp(self):
        self.clinic = Clinic.objects.create(
            name="Test Clinic",
            address="123 Test Address",
            clinic_serial="CLINIC001",
            accepted=True
        )

    def test_clinic_creation(self):
        clinic = Clinic.objects.create(
            name="New Clinic",
            address="456 New Street",
            clinic_serial="CLINIC002"
        )
        self.assertEqual(clinic.name, "New Clinic")
        self.assertEqual(clinic.address, "456 New Street")
        self.assertEqual(clinic.clinic_serial, "CLINIC002")
        self.assertFalse(clinic.accepted)

    def test_clinic_serial_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Clinic.objects.create(
                name="Duplicate Serial Clinic",
                address="456 Another Street",
                clinic_serial="CLINIC001"
            )

    def test_clinic_str_representation(self):
        self.assertEqual(str(self.clinic),
                         "Test Clinic in address: 123 Test Address")
