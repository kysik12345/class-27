from .views import *
from django.urls import path
from users.views import register,log_in,log_out, user_detail

urlpatterns = [
    path("register/",register, name='register'),
    path("login/", log_in, name='login'),
    # path("change_password/", change_password, name='change_password'),
    path("logout/", log_out, name='logout'),
    path('detail/<int:pk>/', user_detail, name='detail'),
]