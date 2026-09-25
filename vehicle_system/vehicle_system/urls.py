"""
URL configuration for vehicle_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.contrib import admin
from inventory.views import *
urlpatterns = [

    # --------------------
    # FRONTEND
    # --------------------

    path('', home, name='home'),

    path(
        'vehicles/',
        vehicle_list,
        name='vehicle_list'
    ),

    path(
        'vehicles/add/',
        vehicle_create,
        name='vehicle_create'
    ),

    path(
        'vehicles/<int:pk>/',
        vehicle_detail,
        name='vehicle_detail'
    ),

    path(
        'vehicles/<int:pk>/edit/',
        vehicle_edit,
        name='vehicle_edit'
    ),

    path(
        'vehicles/<int:pk>/delete/',
        vehicle_delete,
        name='vehicle_delete'
    ),

    path(
        'bookings/',
        booking_list,
        name='booking_list'
    ),

    path(
        'bookings/add/',
        booking_create,
        name='booking_create'
    ),

    path(
        'bookings/<int:pk>/',
        booking_detail,
        name='booking_detail'
    ),


    # --------------------
    # REST API
    # --------------------

    path(
        'api/vehicles/',
        VehicleListCreateView.as_view(),
        name='vehicle-list'
    ),

    path(
        'api/vehicles/<int:pk>/',
        VehicleDetailView.as_view(),
        name='vehicle-detail'
    ),

    path(
        'api/bookings/',
        BookingListCreateView.as_view(),
        name='booking-list'
    ),

    path(
        'api/bookings/<int:pk>/',
        BookingDetailView.as_view(),
        name='booking-detail'
    ),
]
