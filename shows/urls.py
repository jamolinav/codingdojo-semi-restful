from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('shows/', views.shows),
    path('favicon.ico', views.okay),
    path('initialize/', views.make_data, name="make_data"),
    path('new_show/', views.new_show),
    path('create_show/', views.create_show),
    path('create_show/checkEmail/',views.checkEmail),
    path('show/<int:id>/',views.show_show),
    path('edit/<int:id>/',views.edit_show),
    path('update/<int:id>/',views.update_show),
    path('delete/<int:id>/',views.delete_show),
]