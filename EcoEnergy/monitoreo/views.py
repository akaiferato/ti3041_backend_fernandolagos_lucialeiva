from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

from .models import Organization, Category, Zone, Device, Measurement, Alert


def dashboard(request):
    devices_categories = Category.objects.annotate(n_devices=Count('devices')).order_by('name')
    
    devices_zones = Zone.objects.annotate(n_devices=Count('devices')).order_by('devices_zone')

    week_ago = timezone.now() - timedelta(days=7)
    week_alerts = Alert.objects.filter(alerts__date__gte=week_ago)
    alert_summary = {
            'graves' : week_alerts.filter(level=Alert.Level.GRAVE).count(),
            'altas' : week_alerts.filter(level=Alert.Level.ALTA).count(),
            'medias' : week_alerts.filter(level=Alert.Level.MEDIA).count()
            }
    
    last10_measures = Measurement.objects.order_by('-timestamp')[:10]

    context = {
            "devices_categories":devices_categories,
            "devices_zones" : devices_zones,
            "alert_summary" : alert_summary,
            "last10_measures" : last10_measures
            }

    return render(request, "monitoreo/dashboard.html", context)

def device_list(request):
    devices = Device.objects.select_related('category', 'zone')
    
    category_id = request.GET.get('category')
    if category_id:
        devices = devices.filter(category__id=category_id)

    categories = Category.objects.all()

    context = {
        'devices': devices,
        'categories': categories,
        'marked_category': int(category_id) if category_id else None
    }
    return render(request, 'monitoreo/lista_dispositivos.html', context)

def device_details(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    
    measurements = device.measurements.order_by('-timestamp')[:50]
    alerts = device.measurements.alerts.order_by('-timestamp')

    context = {
        'device': device,
        'measurements': measurements,
        'alerts': alerts
    }
    return render(request, 'monitoreo/detalle_dispositivo.html', context)

def measurements_list(request):
    measurements = Measurement.objects.select_related('device').order_by('-timestamp')

    context = {'measurements' : measurements}

    return render(request, "monitoreo/lista_mediciones.html", context)
