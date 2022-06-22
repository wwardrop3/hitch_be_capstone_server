# Generated by Django 4.0.5 on 2022-06-19 04:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverPassengerTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='DriverTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_place', models.TextField()),
                ('destination_place', models.TextField()),
                ('creation_date', models.DateTimeField()),
                ('start_date', models.DateTimeField()),
                ('completion_date', models.DateTimeField(null=True)),
                ('detour_radius', models.IntegerField()),
                ('trip_distance', models.FloatField()),
                ('expected_travel_time', models.FloatField()),
                ('trip_summary', models.TextField(null=True)),
                ('seats', models.IntegerField()),
                ('completed', models.BooleanField()),
                ('path', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=201)),
                ('profile_image_url', models.CharField(max_length=201)),
                ('created_on', models.DateTimeField()),
                ('active', models.BooleanField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TripTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver_trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hitchapi.drivertrip')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hitchapi.tag')),
            ],
        ),
        migrations.CreateModel(
            name='PassengerTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_place', models.TextField()),
                ('destination_place', models.TextField()),
                ('creation_date', models.DateTimeField()),
                ('start_date', models.DateTimeField()),
                ('completion_date', models.DateTimeField(null=True)),
                ('trip_distance', models.FloatField()),
                ('expected_travel_time', models.FloatField()),
                ('trip_summary', models.TextField(null=True)),
                ('path', models.TextField()),
                ('is_approved', models.BooleanField()),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passenger_trip_destination', to='hitchapi.location')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passenger_trip_origin', to='hitchapi.location')),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hitchapi.member')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateField()),
                ('is_read', models.BooleanField()),
                ('message_text', models.TextField()),
                ('driver_trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hitchapi.drivertrip')),
                ('passenger_trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hitchapi.passengertrip')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='hitchapi.member')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='hitchapi.member')),
            ],
        ),
        migrations.CreateModel(
            name='DriverTripRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('review', models.TextField()),
                ('driver_trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hitchapi.drivertrip')),
                ('passenger_trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hitchapi.passengertrip')),
            ],
        ),
        migrations.AddField(
            model_name='drivertrip',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_destination', to='hitchapi.location'),
        ),
        migrations.AddField(
            model_name='drivertrip',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hitchapi.member'),
        ),
        migrations.AddField(
            model_name='drivertrip',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_origin', to='hitchapi.location'),
        ),
        migrations.AddField(
            model_name='drivertrip',
            name='passenger_trips',
            field=models.ManyToManyField(related_name='driver_trips', through='hitchapi.DriverPassengerTrip', to='hitchapi.passengertrip'),
        ),
        migrations.AddField(
            model_name='drivertrip',
            name='tags',
            field=models.ManyToManyField(related_name='trips', through='hitchapi.TripTag', to='hitchapi.tag'),
        ),
        migrations.AddField(
            model_name='driverpassengertrip',
            name='driver_trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hitchapi.drivertrip'),
        ),
        migrations.AddField(
            model_name='driverpassengertrip',
            name='passenger_trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hitchapi.passengertrip'),
        ),
    ]
