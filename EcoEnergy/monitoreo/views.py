from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

from .models import Category, Zone, Device, Measurement, Alert


def dashboard(request):
    devices_categories = Category.objects.annotate(n_devices=Count('devices')).order_by('name')
    devices_zones = Zone.objects.annotate(n_devices=Count('devices')).order_by('device_zone')
    
    week_ago = timezone.now() - timedelta(days=7)
    week_alerts = Alert.objects.filter(measurement__date__gte=week_ago)
    alert_summary = {
            'graves': week_alerts.filter(level=Alert.Level.GRAVE).count(),
            'altas': week_alerts.filter(level=Alert.Level.ALTA).count(),
            'medias': week_alerts.filter(level=Alert.Level.MEDIA).count()
            }
    
    last10_measures = Measurement.objects.order_by('-date')[:10]

    context = {
            "devices_categories": devices_categories,
            "devices_zones": devices_zones,
            "alert_summary": alert_summary,
            "last10_measures": last10_measures
            }

    return render(request, "dashboard.html", context)


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
    return render(request, 'device_list.html', context)


def device_details(request, id):
    device = get_object_or_404(Device, pk=id)
    measurements = device.measurements.order_by('-date')[:50]
    alerts = Alert.objects.filter(measurement__device=device).order_by('-measurement__date')

    context = {
        'device': device,
        'measurements': measurements,
        'alerts': alerts
    }
    return render(request, 'device_details.html', context)

def measurement_list(request):
    measurements = Measurement.objects.select_related('device').order_by('-date')
    context = {'measurements': measurements}

    return render(request, "measurement_list.html", context)
