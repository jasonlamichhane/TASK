from django.contrib import admin
from django.urls import path, re_path, include
from users.views import RegisterView, VerifyEmail, LoginAPIView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from car.views import CarSpecificationViewSet, CarPlanViewSet

router = DefaultRouter()
router.register('specification',CarSpecificationViewSet, basename='car')
router.register('plan',CarPlanViewSet, basename='plan')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    path('car/',include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('login/', LoginAPIView.as_view(), name='login'),
]
