from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.user_registration, name="registration"),
    path("sign_in/", views.user_sign_in, name="signIn"),
]
