from . import views

from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('', views.UserLoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name="profile"),
    path('return/<int:pk>', views.return_car, name='return')
]
 