from django.db import models

class Entry(models.Model):
    id = models.IntegerField(primary_key=True)
    esearch = models.CharField(max_length=128)
    eentry = models.CharField(max_length=128)
    tentry = models.CharField(max_length=1028)
    ecat = models.CharField(max_length=10)
