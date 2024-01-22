from django.urls import path

from . import views

app_name = 'car'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('list/', views.ListCars.as_view(), name='list'),
    path('details/<int:pk>', views.CarDetailView.as_view(), name='detail'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('search_results/', views.SearchResultView.as_view(), name='search_result'),
    path('rent/<int:pk>/', views.rent_car, name='rent'),
    path('checkout/<int:rental_id>/', views.checkout, name='checkout'),
    path('complete_order/', views.complete_order, name='complete'),
]
