from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsMedicOrAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_staff or user.is_superuser:
            return True
        try:
            return user.medic.accepted and user.is_medic
        except Exception:
            return False


class IsPatientOrAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_staff or user.is_superuser:
            return True
        try:
            return user.patient and user.is_patient
        except Exception:
            return False


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user

        return obj.user == user or user.is_staff or user.is_superuser


class IsAppointmentRelated(BasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff or user.is_superuser:
            return True
        try:
            if user.is_patient and user.patient:
                return obj.patient.user == user
            elif user.is_medic and user.medic:
                return obj.time.medic.user == user
        except Exception:
            return False

        return False
