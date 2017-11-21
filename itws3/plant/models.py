from __future__ import unicode_literals
from django.db import models
# Create your models here.
class Plant(models.Model):
	plantid= models.CharField(max_length=250)
	longitude = models.CharField(max_length=250)
	latitude = models.CharField(max_length=250)
	automode = models.CharField(max_length=200,default='off')
	motorstate = models.CharField(max_length=200,default='off')
	def __str__(self):
		return str(str(self.pk)+","+str(self.automode) +","+str(self.motorstate))
class Sensors(models.Model):
	plant=models.ForeignKey(Plant,on_delete=models.CASCADE)
	tem_value = models.CharField(max_length=250)
	hum_value = models.CharField(max_length=250)
	soil_mois = models.CharField(max_length=250)
	wat_lvl = models.CharField(max_length=250) 
	time = models.CharField(max_length=250)
	rain = models.CharField(max_length=10 )
	def __str__(self):
		return str(self.tem_value + "," + self.hum_value + "," + self.soil_mois+','+self.wat_lvl+','+self.time+','+self.rain)
