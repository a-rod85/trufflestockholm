from django.urls import path
from contact import views

urlpatterns = [
    path("", views.contact, name="contact"),
    path("food_menu", views.FoodMenu.as_view())
]
