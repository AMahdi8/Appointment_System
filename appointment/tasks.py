from celery import shared_task
from django.utils import timezone
from .models import Appointment
from .utils import send_sms_to_medic

@shared_task
def send_appointment_sms():
    today = timezone.now().date()
    tomorrow = today + timezone.timedelta(days=1)

    appointments = Appointment.objects.filter(appointment_datetime__date=tomorrow)

    medic_appointments = {}
    for appointment in appointments:
        medic = appointment.time.medic
        if medic not in medic_appointments:
            medic_appointments[medic] = []
        medic_appointments[medic].append(appointment)

    for medic, appointments in medic_appointments.items():
        message = f"Appointments for {tomorrow}:\n"
        for appointment in appointments:
            message += f"- {appointment.patient} at {appointment.appointment_datetime.strftime('%H:%M')}\n"
        

        send_sms_to_medic(medic.phone_number, message)