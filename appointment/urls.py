from rest_framework.routers import DefaultRouter

from appointment.views import AppointmentViewSet, PrescriptionViewSet

router = DefaultRouter()
router.register('appointment', AppointmentViewSet, basename='appointment')
router.register('prescription', PrescriptionViewSet, basename='prescription')

urlpatterns = router.urls
