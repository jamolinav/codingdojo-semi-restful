from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('favicon.ico', views.okay),
    path('initialize/', views.make_data, name="make_data"),
    path('new_show/', views.new_show),
    path('create_show/', views.create_show),
]