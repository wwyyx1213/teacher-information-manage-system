from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'teachers', TeacherViewSet, basename='teacher')

urlpatterns = [
    path('', include(router.urls)),
]
