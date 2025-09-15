from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class Organization(BaseModel):
    name = models.CharField(max_length=20)
    rut = models.CharField(max_length=15)
    field = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name


class Zone(BaseModel):
    device_zone = models.CharField(max_length=20)
    coordinates = models.CharField(max_length=50)

    def __str__(self):
        return self.device_zone


class Device(BaseModel):
    name = models.CharField(max_length=20)
    state = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='devices')
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='devices')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='devices')

    def __str__(self):
        return self.name


class Measurement(BaseModel):
    intake = models.IntegerField()
    date = models.DateField(default=timezone.now)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="measurements")

    def __str__(self):
        return str(self.intake)


class Alert(BaseModel):
    class Level(models.TextChoices):
        GRAVE = 'GRV', 'Grave'
        ALTA = 'ALT', 'Alta'
        MEDIA = 'MED', 'Media'

    level = models.CharField(max_length=3, choices=Level.choices)
    description = models.TextField()
    measurement = models.OneToOneField(Measurement, on_delete=models.CASCADE, related_name='alerts')

    def __str__(self):
        return self.level
