
from django.urls import path
from . import views

urlpatterns = [
    path(route='get_cars', view=views.get_cars, name='getcars'),
]
