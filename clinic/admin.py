from django.contrib import admin

from .models import Clinic


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'clinic_serial', 'accepted')
    list_display_links = ('id', )
    list_editable = ('accepted', )
