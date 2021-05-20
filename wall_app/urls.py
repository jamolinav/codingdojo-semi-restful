from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='wall'),
    path('register', views.register, name='register_wall_app'),
    path('login', views.login, name='login_wall_app'),
    path('logout', views.logout, name='logout_wall_app'),
    path('add_message', views.add_message, name='add_message'),
    path('add_message_ajax', views.add_message_ajax, name='add_message_ajax'),
    path('add_comment', views.add_comment, name='add_comment'),
    path('add_comment_ajax', views.add_comment_ajax, name='add_comment_ajax'),
    path('delete_msg/<int:id_msg>/', views.delete_msg, name='delete_msg'),
    path('delete_msg_ajax/<int:id_msg>/', views.delete_msg_ajax, name='delete_msg_ajax'),
    path('delete_comment/<int:id_comment>', views.delete_comment, name='delete_comment'),
    path('delete_comment_ajax/<int:id_comment>', views.delete_comment_ajax, name='delete_comment_ajax'),
]