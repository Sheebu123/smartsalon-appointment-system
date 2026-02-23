from django.urls import path

from .views import (
    appointment_cancel_view,
    appointment_create_view,
    appointment_list_view,
    dashboard_view,
    home_view,
)

app_name = 'appointments'

urlpatterns = [
    path('', home_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('appointments/', appointment_list_view, name='list'),
    path('appointments/new/', appointment_create_view, name='create'),
    path('appointments/<int:appointment_id>/cancel/', appointment_cancel_view, name='cancel'),
]
