from django.urls import path, include
from . import views


app_name = 'images'

urlpatterns = [
    path('create/', views.image_create, name='create'),
]