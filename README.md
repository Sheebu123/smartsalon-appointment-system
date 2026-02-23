# SmartSalon Appointment System

Django backend for managing salon users, appointments, and payments.

## What This Project Does

- User registration, login, and logout
- Appointment booking with future-date validation
- Double-booking prevention for the same stylist and time slot
- Appointment listing, filtering, and cancellation
- One payment record per appointment with mark-as-paid flow
- Simple dashboard with booking and payment counts

## Tech Stack

- Python
- Django
- SQLite (default for local development)

## Project Structure

- `smartsalon_backend/`: Django project settings and root URLs
- `accounts/`: custom user model and account logic
- `appointments/`: appointment-related models and views
- `payments/`: payment-related models and views
- `templates/`: all frontend templates

## Main Routes

- `/`: home page
- `/accounts/register/`: register
- `/accounts/login/`: login
- `/dashboard/`: user dashboard
- `/appointments/`: appointment list and filters
- `/appointments/new/`: create appointment
- `/payments/`: payment list and payment update
- `/admin/`: Django admin panel

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```powershell
pip install django python-dotenv
```

3. Create a `.env` file from `.env.example` and set your secret key:

```env
SECRET_KEY=your-django-secret-key
```

4. Run migrations:

```powershell
python manage.py makemigrations
python manage.py migrate
```

5. Start the development server:

```powershell
python manage.py runserver
```

## Useful Commands

```powershell
python manage.py check
python manage.py test
python manage.py createsuperuser
```

## Notes

- Uses custom auth model: `accounts.User`.
- Default database is SQLite (`db.sqlite3`).
