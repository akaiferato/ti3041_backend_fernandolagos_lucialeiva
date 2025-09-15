from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Measurement(BaseModel):
    intake = models.IntegerField()
    date = models.DateField()
    intake_limit = models.IntegerField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.intake)


class Alert(BaseModel):
    name = models.CharField(max_length=20)
    description = models.TextField()
    measurement = models.OneToOneField(Measurement, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
