from django.urls import path

from .views import payment_list_view, payment_mark_paid_view

app_name = 'payments'

urlpatterns = [
    path('', payment_list_view, name='list'),
    path('<int:payment_id>/mark-paid/', payment_mark_paid_view, name='mark_paid'),
]
