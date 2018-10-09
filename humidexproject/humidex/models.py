from django.db import models

# Create your models here.
class Measurement(models.Model):
	time = models.DateTimeField(auto_now_add=True)
	room = models.CharField(max_length=30)
	value = models.IntegerField()