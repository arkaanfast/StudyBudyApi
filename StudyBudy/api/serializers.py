from rest_framework import serializers
from . import models


class StudentSerializer(serializers.ModelSerializer):
    # Student serializer to convert the data to json :)
    class Meta:
        model = models.User
        fields = ["user_id", "username", "email", "phone_number", "usn"]


class TeacherSerializer(serializers.ModelSerializer):
    # Teacher serializer to convert the data to json :)
    class Meta:
        model = models.User
        fields = ["user_id", "username", "email", "phone_number"]


class StudentQueriesSerializer(serializers.ModelSerializer):
    # Studnet Queries  serializer to convert the data to json :)
    class Meta:
        model = models.StudentQueries
        fields = ["question", "answer"]
