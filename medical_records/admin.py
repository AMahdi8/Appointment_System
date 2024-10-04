from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import MedicalRecord


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'medic_link', 'patient_link',
                    'illnes_subject', 'hospitalized')
    list_filter = ('medic', 'patient', 'hospitalized')
    search_fields = ('medic__user__first_name', 'medic__user__last_name',
                     'patient__user__first_name', 'patient__user__last_name', 'illnes_subject')
    list_display_links = ('id', )

    def medic_link(self, obj):
        url = reverse('admin:user_medic_change', args=[obj.medic.id])
        return format_html('<a href="{}">{}</a>', url, obj.medic)

    medic_link.short_description = 'Medic'

    def patient_link(self, obj):
        url = reverse('admin:user_patient_change', args=[obj.patient.id])
        return format_html('<a href="{}">{}</a>', url, obj.patient.user)

    patient_link.short_description = 'Patient'
