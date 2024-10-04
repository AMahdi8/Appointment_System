from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .models import Medic, Patient, TimeSlot, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'first_name',
                    'last_name', 'age', 'is_medic', 'is_patient')
    list_editable = ('is_medic', 'is_patient')
    list_filter = ('is_superuser', 'is_staff', 'is_medic', 'is_patient')
    search_fields = ('phone_number', 'first_name', 'last_name')
    ordering = ('id',)

    fieldsets = (
        (_('Personal Info'), {
         'fields': ('phone_number', 'first_name', 'last_name', 'age')}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'is_medic', 'is_patient')}),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),
    )


@ admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_link', 'blood_group')
    list_filter = ('blood_group',)
    list_display_links = ('id', 'user_link')
    search_fields = ('user__phone_number',
                     'user__first_name', 'user__last_name')
    ordering = ('user__id',)

    def user_link(self, obj):
        url = reverse('admin:user_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user)

    user_link.short_description = 'User'


@ admin.register(Medic)
class MedicAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_link', 'specialization', 'accepted')
    list_filter = ('specialization', 'accepted')
    list_display_links = ('id', 'user_link')
    search_fields = ('user__phone_number',
                     'user__first_name', 'user__last_name')
    list_editable = ('accepted',)
    ordering = ('user__id',)

    def user_link(self, obj):
        url = reverse('admin:user_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user)

    user_link.short_description = 'User'


@ admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'medic_link', 'clinic_link', 'day_of_week', 'start_time',
                    'end_time', 'avg_visit_time', 'avg_patient_visit', 'is_active')
    list_filter = ('medic', 'clinic', 'day_of_week', 'is_active')
    search_fields = ('medic__user__first_name',
                     'medic__user__last_name', 'clinic__name')
    list_display_links = ('id', )
    list_editable = ('is_active', )

    def medic_link(self, obj):
        url = reverse('admin:user_medic_change', args=[obj.medic.id])
        return format_html('<a href="{}">{}</a>', url, obj.medic)

    medic_link.short_description = 'Medic'

    def clinic_link(self, obj):
        url = reverse('admin:clinic_clinic_change', args=[obj.clinic.id])
        return format_html('<a href="{}">{}</a>', url, obj.clinic.name)

    clinic_link.short_description = 'Clinic'
