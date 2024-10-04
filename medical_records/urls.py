from rest_framework.routers import DefaultRouter

from medical_records.views import MedicalRecordViewSet

router = DefaultRouter()
router.register('medical_record', MedicalRecordViewSet,
                basename='medical_record')

urlpatterns = router.urls
