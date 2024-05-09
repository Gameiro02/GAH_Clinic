from django.db import models

class Appointment(models.Model):
    user_id = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=50)
