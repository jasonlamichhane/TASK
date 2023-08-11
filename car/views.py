from django.shortcuts import render
from rest_framework import viewsets
from .models import CarSpecification, CarPlan
from .serializers import CarSpecificationSerializer, CarPlanSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .permissions import isOwner

from rest_framework.pagination import PageNumberPagination

from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

class CarPlanViewSet(viewsets.ModelViewSet):
    queryset = CarPlan.objects.all()
    serializer_class = CarPlanSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CarSpecificationViewSet(viewsets.ModelViewSet):
    queryset = CarSpecification.objects.all()
    serializer_class = CarSpecificationSerializer
    permission_classes = (permissions.IsAuthenticated,isOwner)
    pagination_class = PageNumberPagination

    def create(self, request,*args, **kwargs):
            carplan_id = request.data.get('car_plan')
            try:
                carplan = CarPlan.objects.get(id=carplan_id)
            except ObjectDoesNotExist:
                return Response({'error': 'Invalid car_plan ID'}, status=status.HTTP_400_BAD_REQUEST)

            carspecs = CarSpecification.objects.create(
            car_plan=carplan,
            car_brand=request.data.get('car_brand'),
            car_model=request.data.get('car_model'),
            manufacture_year=request.data.get('manufacture_year')
        )
            
            serializer = CarSpecificationSerializer(carspecs)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
