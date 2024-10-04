from django.db import models
from django.utils.translation import gettext_lazy as _


class Clinic(models.Model):
    name = models.CharField(
        _('name'),
        max_length=255,
    )

    address = models.TextField(_('address'))

    clinic_serial = models.CharField(
        _('clinic_serial'),
        max_length=30,
        unique=True
    )

    image = models.ImageField(
        _('image'),
        blank=True,
        null=True,
        upload_to='media/clinics/'
    )

    accepted = models.BooleanField(_('accepted'), default=False)

    def __str__(self) -> str:
        return f"{self.name} in address: {self.address}"
