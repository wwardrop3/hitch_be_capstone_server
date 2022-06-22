DROP TABLE hitchapi_driver_trips

DROP TABLE hitchapi_location


DELETE FROM auth_user
WHERE id <2

DELETE FROM hitchapi_triptag
WHERE driver_trip_id >0

DELETE FROM hitchapi_drivertrip
WHERE id >0

DELETE FROM hitchapi_driverpassengertrip
WHERE id >0


DELETE FROM hitchapi_passengertrip
WHERE id >0

DELETE FROM authtoken_token
WHERE user_id <2

DELETE FROM hitchapi_message
WHERE id >0