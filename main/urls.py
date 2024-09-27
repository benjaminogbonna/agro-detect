from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('c', views.camera, name='c'),
    path('anthracnose', views.anthracnose, name='anthracnose'),
    path('cercospora-leaf-spot', views.cls, name='cls'),
    path('phosphorus-deficiency', views.pd, name='pd'),

    path('api/prediction/', views.prediction),
]
