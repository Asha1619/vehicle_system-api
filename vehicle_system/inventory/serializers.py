from rest_framework import serializers
from .models import Vehicle, Booking
from django.utils import timezone

class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['total_amount']

    def validate_customer_phone(self, value):

        if not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only digits."
            )

        if len(value) != 10:
            raise serializers.ValidationError(
                "Phone number must be exactly 10 digits."
            )

        return value

    def validate(self, data):

        start_date = data.get('start_date')
        end_date = data.get('end_date')
        vehicle = data.get('vehicle')

       

        if start_date < timezone.now().date():
            raise serializers.ValidationError(
                "Start date cannot be in the past."
            )

        if end_date <= start_date:
            raise serializers.ValidationError(
                "End date must be after start date."
            )

        
        overlapping_bookings = Booking.objects.filter(
            vehicle=vehicle,
            start_date__lt=end_date,
            end_date__gt=start_date
        )

        if self.instance:
            overlapping_bookings = overlapping_bookings.exclude(
                id=self.instance.id
            )

        if overlapping_bookings.exists():
            raise serializers.ValidationError(
                "Vehicle is already booked for these dates."
            )

        return data

    def create(self, validated_data):

        vehicle = validated_data['vehicle']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']

        days = (end_date - start_date).days

        total_amount = days * vehicle.price_per_day

        booking = Booking.objects.create(
            **validated_data,
            total_amount=total_amount
        )

        vehicle.is_available = False
        vehicle.save()

        return booking