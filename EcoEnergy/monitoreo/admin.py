from django.contrib import admin

from .models import Organization, Category, Zone, Device, Measurement, Alert

admin.site.register([Organization, Category, Zone, Device, Measurement, Alert])
