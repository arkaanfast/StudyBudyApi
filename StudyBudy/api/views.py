from allennlp import common
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import *
from .serializers import *

from .services import *

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
                data={"success": "created student account", "token": token.key},
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
                data={"error": "created teacher account", "token": token.key},
                status=status.HTTP_201_CREATED,
            )
    except Exception:
        return Response(
            data={"error": "Email or Usn or phone number already Exists"},
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
                    data={"error": "Not Registerd"}, status=status.HTTP_404_NOT_FOUND
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
                    data={"error": "Not Registerd"}, status=status.HTTP_404_NOT_FOUND
                )
    except User.DoesNotExist:
        return Response(
            data={"error": "Not Registerd"}, status=status.HTTP_404_NOT_FOUND
        )


# Post the question and get the answer /api/student_queries
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_student_queries(request):
    question = request.data["question"]
    # Checks if the question has been asked earlier or not
    check = check_if_already_asked(question)

    # if the question has been asked
    if check:
        # store the answer in the users queries database
        try:
            # if the question has been already asked by the same user
            student_query = StudentQueries.objects.get(question=question)
            query_serailizer = StudentQueriesSerializer(student_query)
            return Response(data=query_serailizer.data, status=status.HTTP_200_OK)
        except StudentQueries.DoesNotExist:
            student_query = StudentQueries(
                student_id=request.user, question=question, answer=check
            )
            student_query.save()
            # Create a studentQuery object for the student after getting the answers for the question.
            query_serailizer = StudentQueriesSerializer(student_query)
            return Response(data=query_serailizer.data, status=status.HTTP_200_OK)

    # if the question has not been asked yet
    else:
        answer = get_answer(question)
        # if the answer to the question exists
        if answer:
            student_query = StudentQueries(
                student_id=request.user, question=question, answer=answer
            )
            student_query.save()
            common_questions = CommonQuestions(question=question, answer=answer)
            common_questions.save()
            # Create a studentQuery object for the student after getting the answers for the question.
            query_serailizer = StudentQueriesSerializer(student_query)
            return Response(data=query_serailizer.data, status=status.HTTP_200_OK)

        # if the answer does not exist
        else:
            return Response(
                data={
                    "error": "The answer for the question you asked does not exist now we are still improving our algo"
                },
                status=status.HTTP_404_NOT_FOUND,
            )


# Get list of a student query /api/student_queries_list
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_student_queries(request):
    student_query = StudentQueries.objects.filter(student_id=request.user)
    if len(student_query) == 0:
        return Response(data={"response": "no queries yet"}, status=status.HTTP_200_OK)
    else:
        query_serailizer = StudentQueriesSerializer(student_query, many=True)
        return Response(data=query_serailizer.data, status=status.HTTP_200_OK)
