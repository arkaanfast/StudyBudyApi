from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import *
from .serializers import *

# Register url:-/api/register/


@api_view(["POST"])
def user_registration(request):
    try:
        if request.data["is_student"]:
            student = User(
                username=request.data["username"],
                email=request.data["email"],
                phone_number=request.data["phone_number"],
                usn=request.data["usn"].upper(),
            )
            student.set_password(request.data["password"])
            student.save()
            authenticate(
                username=request.data["email"], password=request.data["password"]
            )
            token = Token.objects.get(user=student)
            return Response(
                data={"response": "created student account", "token": token.key},
                status=status.HTTP_201_CREATED,
            )
        else:
            teacher = User(
                username=request.data["username"],
                email=request.data["email"],
                phone_number=request.data["phone_number"],
                is_staff=True,
            )
            teacher.set_password(request.data["password"])
            teacher.save()
            authenticate(
                username=request.data["email"], password=request.data["password"]
            )
            token = Token.objects.get(user=teacher)
            return Response(
                data={"response": "created teacher account", "token": token.key},
                status=status.HTTP_201_CREATED,
            )
    except Exception:
        return Response(
            data={"response": "already registered"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# Sign in :-/api/sign_in/


@api_view(["POST"])
def user_sign_in(request):
    data = {}
    try:
        if request.data["is_student"]:
            st = User.object.get(usn=request.data["usn"])
            student = authenticate(username=st.email, password=request.data["password"])
            if student is not None:
                token = Token.objects.get(user=student)
                student_serializer = StudentSerializer(student)
                data["student_details"] = student_serializer.data
                data["token"] = token.key
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                return Response(
                    data={"response": "Not Registerd"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            teacher = authenticate(
                username=request.data["email"], password=request.data["password"]
            )
            if teacher is not None:
                token = Token.objects.get(user=teacher)
                teacher_serializer = TeacherSerializer(teacher)
                data["teacher_details"] = teacher_serializer.data
                data["token"] = token.key
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                return Response(
                    data={"response": "Not Registerd"}, status=status.HTTP_404_NOT_FOUND
                )
    except User.DoesNotExist:
        return Response(
            data={"response": "Not Registerd"}, status=status.HTTP_404_NOT_FOUND
        )
