from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
import json

from .models import Car, RentalHistory
from .forms import RentalForm

# Create your views here.


class HomeView(generic.TemplateView):
    template_name = 'home.html'


class ListCars(LoginRequiredMixin, generic.ListView):
    model = Car
    template_name = 'list.html'
    context_object_name = 'cars'

    def get_queryset(self):
        query = Car.objects.filter(availability=True)
        return query


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car
    template_name = 'detail.html'


class SearchView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'search.html'


class SearchResultView(LoginRequiredMixin, generic.ListView):
    model = Car
    template_name = 'search_result.html'
    context_object_name = 'cars'
    empty_message = 'No cars found.'

    def get_queryset(self):
        make = self.request.GET.get("make")
        model = self.request.GET.get("model")
        price = self.request.GET.get("price")
        location = self.request.GET.get("location")
        fuel = self.request.GET.get("fuel")

        queryset = Car.objects.all()

        if make:
            queryset = queryset.filter(make__icontains=make)
        if model:
            queryset = queryset.filter(model__icontains=model)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if fuel:
            queryset = queryset.filter(fuel__icontains=fuel)
        if price:
            try:
                price = Decimal(price)
                queryset = queryset.filter(price__lte=price)
            except (ValueError, TypeError):
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['cars']:
            context['empty_message'] = self.empty_message
        return context


@login_required
def rent_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    user = request.user

    if request.method == 'POST':
        form = RentalForm(request.POST)

        if form.is_valid():
            rental = form.save(commit=False)
            rental.car = car
            rental.user = user
            rental.save()

            rental.total_price()

            return redirect('car:checkout', rental_id=rental.id)
    else:
        form = RentalForm(initial={'car': car, 'user': user})

    return render(request, 'rental_form.html', {'form': form, 'car': car})


@login_required
def checkout(request, rental_id):
    rental = get_object_or_404(RentalHistory, pk=rental_id)
    total_price = rental.rental_amount

    if request.method == 'POST':
        return redirect('car:detail', pk=rental.car.id)

    return render(request, 'checkout.html', {'rental': rental, 'total': total_price})


def complete_order(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        rental_id = payload.get('rental_id')
        if rental_id is not None:
            rental = RentalHistory.objects.get(pk=rental_id)
            rental.mark_as_paid()

            rental.car.availability = False
            rental.car.save()

            return redirect('car:list')

    return HttpResponseBadRequest('Invalid request method')
