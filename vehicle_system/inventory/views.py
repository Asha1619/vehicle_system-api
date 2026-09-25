from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import VehicleSerializer, BookingSerializer
from django.contrib import messages


def home(request):
    vehicles = Vehicle.objects.all()

    total_vehicles = vehicles.count()
    available_vehicles = vehicles.filter(is_available=True).count()
    total_bookings = Booking.objects.count()

    context = {
        'vehicles': vehicles[:6],
        'total_vehicles': total_vehicles,
        'available_vehicles': available_vehicles,
        'total_bookings': total_bookings,
    }

    return render(
        request,
        'home.html',
        context
    )

def vehicle_list(request):
    vehicles = Vehicle.objects.all()

    brand = request.GET.get('brand')
    fuel_type = request.GET.get('fuel_type')
    is_available = request.GET.get('is_available')

    if brand:
        vehicles = vehicles.filter(brand__icontains=brand)

    if fuel_type:
        vehicles = vehicles.filter(fuel_type=fuel_type)

    if is_available == 'true':
        vehicles = vehicles.filter(is_available=True)

    if is_available == 'false':
        vehicles = vehicles.filter(is_available=False)

    context = {
        'vehicles': vehicles,
        'selected_brand': brand or '',
        'selected_fuel_type': fuel_type or '',
        'selected_availability': is_available or '',
    }

    return render(request,'vehicle_list.html',context)


def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)

    bookings = vehicle.bookings.all().order_by('-start_date')

    context = {
        'vehicle': vehicle,
        'bookings': bookings,
    }

    return render(
        request,
        'vehicle_detail.html',
        context
    )


def vehicle_create(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        brand = request.POST.get('brand')
        year = request.POST.get('year')
        price_per_day = request.POST.get('price_per_day')
        fuel_type = request.POST.get('fuel_type')

        Vehicle.objects.create(
            name=name,
            brand=brand,
            year=year,
            price_per_day=price_per_day,
            fuel_type=fuel_type,
            is_available=True
        )

        messages.success(
            request,
            'Vehicle added successfully.'
        )

        return redirect('vehicle_list')

    return render(
        request,
        'vehicle_form.html'
    )


def vehicle_edit(request, pk):

    vehicle = get_object_or_404(Vehicle, pk=pk)

    if request.method == 'POST':

        vehicle.name = request.POST.get('name')
        vehicle.brand = request.POST.get('brand')
        vehicle.year = request.POST.get('year')
        vehicle.price_per_day = request.POST.get('price_per_day')
        vehicle.fuel_type = request.POST.get('fuel_type')

        vehicle.save()

        messages.success(
            request,
            'Vehicle updated successfully.'
        )

        return redirect(
            'vehicle_detail',
            pk=vehicle.id
        )

    context = {
        'vehicle': vehicle
    }

    return render(
        request,
        'vehicle_form.html',
        context
    )


def vehicle_delete(request, pk):

    vehicle = get_object_or_404(Vehicle, pk=pk)

    if request.method == 'POST':
        vehicle.delete()

        messages.success(
            request,
            'Vehicle deleted successfully.'
        )

        return redirect('vehicle_list')

    return redirect(
        'vehicle_detail',
        pk=vehicle.id
    )


def booking_list(request):

    bookings = Booking.objects.select_related(
        'vehicle'
    ).all().order_by('-start_date')

    context = {
        'bookings': bookings
    }

    return render(
        request,
        'booking_list.html',
        context
    )


def booking_create(request):

    vehicles = Vehicle.objects.filter(
        is_available=True
    )

    if request.method == 'POST':

        vehicle_id = request.POST.get('vehicle')
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        vehicle = get_object_or_404(
            Vehicle,
            id=vehicle_id
        )

        # Use the same serializer validation
        serializer = BookingSerializer(
            data={
                'vehicle': vehicle.id,
                'customer_name': customer_name,
                'customer_phone': customer_phone,
                'start_date': start_date,
                'end_date': end_date,
            }
        )

        if serializer.is_valid():

            serializer.save()

            messages.success(
                request,
                'Booking created successfully.'
            )

            return redirect('booking_list')

        context = {
            'vehicles': vehicles,
            'errors': serializer.errors,
            'form_data': request.POST,
        }

        return render(
            request,
            'booking_form.html',
            context
        )

    return render(
        request,
        'booking_form.html',
        {
            'vehicles': vehicles
        }
    )


def booking_detail(request, pk):

    booking = get_object_or_404(
        Booking.objects.select_related('vehicle'),
        pk=pk
    )

    context = {
        'booking': booking
    }

    return render(
        request,
        'booking_detail.html',
        context
    )







class VehicleListCreateView(APIView):

    def get(self, request):

        vehicles = Vehicle.objects.all()
        brand = request.query_params.get('brand')
        fuel_type = request.query_params.get('fuel_type')
        is_available = request.query_params.get('is_available')

        if brand:
            vehicles = vehicles.filter(brand=brand)

        if fuel_type:
            vehicles = vehicles.filter(fuel_type=fuel_type)

        if is_available:
            vehicles = vehicles.filter(
                is_available=is_available.lower() == 'true'
            )

        serializer = VehicleSerializer(vehicles, many=True)

        return Response(serializer.data)


    def post(self, request):

        serializer = VehicleSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )




class VehicleDetailView(APIView):

    def get(self, request, pk):

        try:
            vehicle = Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            return Response(
                {"error": "Vehicle not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = VehicleSerializer(vehicle)

        return Response(serializer.data)


    def put(self, request, pk):

        try:
            vehicle = Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            return Response(
                {"error": "Vehicle not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = VehicleSerializer(
            vehicle,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


    def delete(self, request, pk):

        try:
            vehicle = Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            return Response(
                {"error": "Vehicle not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        vehicle.delete()

        return Response(
            {"message": "Vehicle deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


class BookingListCreateView(APIView):

    def get(self, request):

        bookings = Booking.objects.all()

        serializer = BookingSerializer(
            bookings,
            many=True
        )

        return Response(serializer.data)


    def post(self, request):

        serializer = BookingSerializer(
            data=request.data
        )

        if serializer.is_valid():

            booking = serializer.save()

            return Response(
                BookingSerializer(booking).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class BookingDetailView(APIView):

    def get(self, request, pk):

        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BookingSerializer(booking)

        return Response(serializer.data)
