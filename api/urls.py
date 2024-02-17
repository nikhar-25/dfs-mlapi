from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('api/', health_check),
    path("api/croprecommend",crop_recommend),
    path("api/suggest",suggestion),
    # path("api/predict",predict),
]