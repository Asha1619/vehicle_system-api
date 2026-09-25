# Vehicle Inventory & Booking API

A REST API built with Django REST Framework for managing vehicles and vehicle bookings.

## Features

- Vehicle CRUD operations
- Vehicle availability management
- Vehicle booking
- Booking date validation
- Prevent overlapping bookings
- Automatic booking amount calculation
- Phone number validation
- Vehicle filtering by brand, fuel type, and availability

## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite / PostgreSQL

## Project Structure


vehicle_system/
├── vehicle_system/
├── inventory/
├── manage.py
├── requirements.txt
└── .env.example

Installation
git clone https://github.com/Asha1619/vehicle_system-api.git
cd vehicle_system

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
Database Setup
python manage.py makemigrations
python manage.py migrate
Run the Project
python manage.py runserver

API will be available at:

http://127.0.0.1:8000/

API Endpoints

Vehicles
Method	Endpoint	Description
GET	/api/vehicles/	List vehicles
POST	/api/vehicles/	Add vehicle
GET	/api/vehicles/<id>/	Vehicle details
PUT	/api/vehicles/<id>/	Update vehicle
DELETE	/api/vehicles/<id>/	Delete vehicle

Bookings

Method	Endpoint	Description
GET	/api/bookings/	List bookings
POST	/api/bookings/	Create booking
GET	/api/bookings/<id>/	Booking details

Filtering

/api/vehicles/?brand=Toyota
/api/vehicles/?fuel_type=Electric
/api/vehicles/?is_available=true


Sample Booking Request
{
    "vehicle": 1,
    "customer_name": "John Doe",
    "customer_phone": "9876543210",
    "start_date": "2026-10-01",
    "end_date": "2026-10-05"
}

The total_amount is calculated automatically based on the number of booking days and the vehicle's daily price.

Booking Validations
Start date cannot be in the past.
End date must be after start date.
Phone number must contain 10 digits.
A vehicle cannot have overlapping bookings.
Vehicle availability is updated after booking.
API Testing

The APIs can be tested using Postman or Swagger.

Screen Recording

Video Link: <add-your-video-link>

Deployment

The API is deployed on Render

Live API:  https://vehicle-system-api.onrender.com

