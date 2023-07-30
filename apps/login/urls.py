from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('verify_user/', views.verify_user, name='verify_user'),
]