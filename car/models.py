from django.db import models

# Create your models here.
class CarPlan(models.Model):
    plan = models.CharField(max_length=255)
    warrenty = models.CharField(max_length=255, null=True, blank=True)

class CarSpecification(models.Model):
    car_plan = models.ForeignKey(CarPlan, on_delete=models.CASCADE)
    car_brand = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255, null=True, blank=True)
    manufacture_year=models.IntegerField()
