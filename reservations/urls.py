from django.urls import path, include
from reservations import views


urlpatterns = [
    path("", views.ReservationsEnquiry.as_view(), name="reservations"),
    path("manage_reservations", views.ManageReservations.as_view(),
    name="manage_reservations",
    )
]
