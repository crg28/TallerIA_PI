from django.urls import path 
from . import views 

urlpatterns = [ 
    path('', views.recomendar_pelicula, name='recommendations'), 
]