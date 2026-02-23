from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PaymentForm
from .models import Payment


@login_required
def payment_list_view(request):
    payments = Payment.objects.select_related('appointment', 'appointment__customer')
    if request.user.role == 'CUSTOMER':
        payments = payments.filter(appointment__customer=request.user)

    return render(request, 'payments/payment_list.html', {'payments': payments})


@login_required
def payment_mark_paid_view(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    can_edit = request.user.role in ['ADMIN', 'STAFF'] or payment.appointment.customer == request.user
    if not can_edit:
        messages.error(request, 'You do not have access to update this payment.')
        return redirect('payments:list')

    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            payment = form.save()
            payment.mark_paid()
            messages.success(request, 'Payment marked as paid.')
        else:
            messages.error(request, 'Please provide valid payment details.')
    return redirect('payments:list')
