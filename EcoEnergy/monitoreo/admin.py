from django.contrib import admin

from .models import Organization, UserOrganization, Category, Zone, Device, Measurement, Alert

admin.site.register([Organization, UserOrganization, Category, Zone, Device, Measurement, Alert])
