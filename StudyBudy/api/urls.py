from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.user_registration, name="registration"),
    path("sign_in/", views.user_sign_in, name="signIn"),
    path("student_querires/", views.post_student_queries, name="studentQueries"),
    path("student_queries_list/", views.get_student_queries, name="studentQueriesList"),
]
