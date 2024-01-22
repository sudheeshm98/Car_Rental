from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from car.models import RentalHistory, Car
from .forms import CustomUserCreationForm, CustomAuthenticationForm

# Create your views here.


class SignUpView(generic.CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('user:login')


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = CustomAuthenticationForm


@login_required
def profile_view(request):
    user = request.user

    current_rental = RentalHistory.objects.filter(
        user=user,
        return_status=False,
    )

    past_rental = RentalHistory.objects.filter(
        user=user,
        return_status=True,
    )

    context = {
        "user": user,
        "current_rentals": current_rental,
        "past_rentals": past_rental
    }

    return render(request, 'profile.html', context)


@login_required
def return_car(request, pk):
    rental = get_object_or_404(RentalHistory, id=pk, user=request.user)

    rental.car.availability = True
    rental.return_status = True
    rental.car.save()
    rental.save()
    
    return redirect(reverse_lazy('user:profile'))
