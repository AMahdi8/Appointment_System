from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import MedicAvailableTimeViewSet, MedicViewSet, PatientViewSet, UserViewSet

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('patient', PatientViewSet, basename='patient')
router.register('medic', MedicViewSet, basename='medic')
router.register('medic_available_times',
                MedicAvailableTimeViewSet, basename='availabe_times')

urlpatterns = [] + router.urls
