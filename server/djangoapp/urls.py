from django.urls import path
from . import views

urlpatterns = [
    path(route='get_dealers', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
    path(route='get_dealer_details/<int:dealer_id>', view=views.get_dealer_details, name='get_dealer_details'),
   path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_details'),
    path(route='add_review', view=views.add_review, name='add_review'),
    path(route='analyze_review', view=views.analyze_review, name='analyze_review'),
]
