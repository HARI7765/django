from django.urls import path
from . import views
urlpatterns=[
    path('index/<int:data>',views.index),
    path('index2',views.index2),
]