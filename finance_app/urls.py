from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload'),
    path('result/', views.display_result, name='result'),
]
