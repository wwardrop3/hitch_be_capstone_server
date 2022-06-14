DROP TABLE hitchapi_driver_trips

DROP TABLE hitchapi_location


DELETE FROM hitchapi_member
WHERE id <9

DELETE FROM hitchapi_triptag
WHERE driver_trip_id >0

DELETE FROM hitchapi_drivertrip
WHERE id >0

DELETE FROM hitchapi_driverpassengertrip
WHERE id >0


DELETE FROM hitchapi_passengertrip
WHERE id >0