from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Student Custom model
class StudentManager(BaseUserManager):
    def create_user(
        self,
        email,
        username,
        password,
        phone_number,
    ):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, phone_number):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            phone_number=phone_number,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    usn = models.CharField(max_length=20, unique=True, null=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    object = StudentManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone_number"]

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class StudentQueries(models.Model):
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)

    def __str__(self):
        return self.student_id.username + " Question :- " + self.question


class CommonQuestions(models.Model):
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question