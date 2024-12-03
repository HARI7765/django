from django.urls import path
from . import views
urlpatterns=[
    path('index',views.index),
    path('admlogin',views.adminlogin),
    path('adminhome',views.adminhome),



]