from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter
from hitchapi.views.auth import login_user, register_user
from hitchapi.views.member_view import MemberView
from hitchapi.views.passenger_trip_view import PassengerTripView
from hitchapi.views.driver_trip_view import DriverTripView



router = DefaultRouter(trailing_slash = False)

router.register(r'driver_trips', DriverTripView, "driver_trip")
router.register(r'passenger_trips', PassengerTripView, "passenger_trip")
router.register(r'members', MemberView, "member")



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', login_user),
    path('register', register_user),
    path('', include(router.urls))
]   
