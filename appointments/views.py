from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from payments.models import Payment

from .forms import AppointmentForm
from .models import Appointment


def home_view(request):
    return render(request, 'home.html')


@login_required
def dashboard_view(request):
    if request.user.role in ['ADMIN', 'STAFF']:
        appointments = Appointment.objects.select_related('customer')
        pending_payments = Payment.objects.filter(status='PENDING').count()
    else:
        appointments = Appointment.objects.filter(customer=request.user)
        pending_payments = Payment.objects.filter(
            appointment__customer=request.user,
            status='PENDING',
        ).count()

    context = {
        'appointments_count': appointments.count(),
        'upcoming_count': appointments.filter(
            status='BOOKED',
            appointment_datetime__gte=timezone.now(),
        ).count(),
        'pending_payments': pending_payments,
    }
    return render(request, 'appointments/dashboard.html', context)


@login_required
def appointment_list_view(request):
    status = request.GET.get('status')
    query = request.GET.get('q')

    appointments = Appointment.objects.select_related('customer')
    if request.user.role == 'CUSTOMER':
        appointments = appointments.filter(customer=request.user)

    if status:
        appointments = appointments.filter(status=status)
    if query:
        appointments = appointments.filter(
            Q(service__icontains=query)
            | Q(stylist_name__icontains=query)
            | Q(customer__username__icontains=query)
        )

    return render(
        request,
        'appointments/appointment_list.html',
        {'appointments': appointments, 'selected_status': status or '', 'search_query': query or ''},
    )


@login_required
def appointment_create_view(request):
    form = AppointmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        appointment = form.save(commit=False)
        appointment.customer = request.user
        appointment.save()

        Payment.objects.create(
            appointment=appointment,
            amount=appointment.get_service_price(),
            status='PENDING',
        )
        messages.success(request, 'Appointment booked. Payment record created.')
        return redirect('appointments:list')

    return render(request, 'appointments/appointment_form.html', {'form': form})


@login_required
def appointment_cancel_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    allowed = request.user.role in ['ADMIN', 'STAFF'] or appointment.customer == request.user
    if not allowed:
        messages.error(request, 'You do not have access to cancel this appointment.')
        return redirect('appointments:list')

    if request.method == 'POST':
        if appointment.status == 'COMPLETED':
            messages.error(request, 'Completed appointments cannot be cancelled.')
        else:
            appointment.status = 'CANCELLED'
            appointment.save(update_fields=['status'])
            messages.info(request, 'Appointment cancelled.')
    return redirect('appointments:list')
