from rest_framework import serializers
from .models import CarPlan, CarSpecification

class CarPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarPlan
        fields = ['id','plan','warrenty']

class CarSpecificationSerializer(serializers.ModelSerializer):
    car_plan = CarPlanSerializer() #nested carplan data
    class Meta:
        model = CarSpecification
        fields = ['id','car_plan','car_brand','car_model','manufacture_year']
