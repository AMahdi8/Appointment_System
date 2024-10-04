from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from appointment.models import Appointment, Prescription

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'prescription_number', 'drugs')
    search_fields = ('prescription_number', )
    list_display_links = ('id', )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_link', 'time_link',
                    'appointment_datetime', 'appointment_number')
    list_display_links = ('id', )
    ordering = ('id',)

    def patient_link(self, obj):
        url = reverse('admin:user_patient_change', args=[obj.patient.id])
        return format_html('<a href="{}">{}</a>', url, obj.patient.user)

    def time_link(self, obj):
        url = reverse('admin:user_timeslot_change', args=[obj.time.id])
        return format_html('<a href="{}">{}</a>', url, obj.time)
