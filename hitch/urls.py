from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter
from hitchapi.serializers.driver_trip_rating_serializer import DriverTripRatingSerializer
from hitchapi.views.auth import login_user, register_user
from hitchapi.views.driver_trip_rating_view import DriverTripRatingView
from hitchapi.views.member_view import MemberView
from hitchapi.views.message_view import MessageView
from hitchapi.views.passenger_trip_view import PassengerTripView
from hitchapi.views.driver_trip_view import DriverTripView
from hitchapi.views.tag_view import TagView



router = DefaultRouter(trailing_slash = False)

router.register(r'driver_trips', DriverTripView, "driver_trip")
router.register(r'passenger_trips', PassengerTripView, "passenger_trip")
router.register(r'members', MemberView, "member")
router.register(r'tags', TagView, "tag")
router.register(r'driver_trip_ratings', DriverTripRatingView, "driver_trip_rating")
router.register(r'messages', MessageView, "message")




urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', login_user),
    path('register', register_user),
    path('', include(router.urls))
]   
