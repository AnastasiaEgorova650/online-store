import json
import os
import logging

from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, hashers
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import ProfileSerializer
from .forms import ProfileForm

User = get_user_model()
logger = logging.getLogger(__name__)


class SignInAPIView(APIView):
    """
    Представление для аутентификации пользователей через логин и пароль.
    """

    def post(self, request):
        try:
            # Логируем запрос для отладки
            logger.info(f"Request data: {request.body}")

            data = json.loads(request.body)
            logger.info(f"Parsed data: {data}")  # Логируем данные после парсинга

        except json.JSONDecodeError:
            logger.error("Invalid JSON format received.")
            return Response(
                {"detail": "Invalid JSON format."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Извлекаем поля из данных
        username = data.get('username')
        password = data.get('password')

        # Проверка на наличие обязательных полей
        if not username or not password:
            logger.warning("Username or password not provided.")
            return Response(
                {"detail": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logger.info(f"User '{username}' successfully logged in.")
            return Response(status=status.HTTP_200_OK)

        logger.warning(f"Invalid login attempt for user: {username}")
        return Response(
            {"detail": "Invalid username or password."},
            status=status.HTTP_401_UNAUTHORIZED
        )


class SingOutAPIView(APIView):
    """
        Представление для выхода пользователя из системы.
    """

    def post(self, request):
        logout(request)
        logger.info(f"User '{request.user.username}' logged out.")
        return Response(status=200)


class SignUpAPIView(APIView):
    """
        Представление для регистрации пользователя в системе.
    """

    def post(self, request):
        try:
            data = json.loads(request.body)
            logger.info(f"Sign up data: {data}")
            username = data['username']
            password = data['password']
            name = data['name']
            email = username + '@django.ru'

            user = User.objects.create(username=username, email=email)
            user.password = hashers.make_password(password)
            user.save()
            UserProfile.objects.create(
                user=user, email=email,
                avatar='avatar_default.png',
            )
            logger.info(f"User '{username}' registered successfully.")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return Response(status=200)
            else:
                logger.error(f"Authentication failed for new user '{username}'.")
                return Response(status=500)
        except Exception as e:
            logger.error(f"Error during sign-up: {str(e)}")
            return Response(status=500)


class ProfileAPIView(APIView):
    """
        Представление для редактирования профиля пользователя в системе.
    """

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            logger.info(f"Retrieved profile data for user '{request.user.username}': {serializer.data}")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving profile for user '{request.user.username}': {str(e)}")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            full_name = request.data['fullName'].split()
            surname = full_name[0]
            name = full_name[1]
            patronymic = full_name[2]
            phone = request.data['phone']

            profile = UserProfile.objects.get(user=request.user)
            profile.name = name
            profile.surname = surname
            profile.patronymic = patronymic
            profile.phone = phone
            profile.save()

            data = {
                "full_name": f"{profile.surname} {profile.name} {profile.patronymic}",
                "email": profile.email,
                "phone": profile.phone,
                "avatar": {
                    "src": profile.avatar.url,
                    "alt": profile.avatar.name,
                },
            }
            logger.info(f"User '{request.user.username}' updated their profile.")
            return JsonResponse(data)
        except Exception as e:
            logger.error(f"Error updating profile for user '{request.user.username}': {str(e)}")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AvatarUpdateAPIView(APIView):
    """
        Представление для редактирования аватарки пользователя в системе.
    """
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            avatar_file = request.FILES.get('avatar')
            avatar_file_path = os.path.join(settings.MEDIA_ROOT, str(profile.avatar))

            if avatar_file:
                if os.path.isfile(avatar_file_path) and profile.avatar != 'avatar_default.png':
                    os.remove(avatar_file_path)

            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                logger.info(f"User '{request.user.username}' updated their avatar.")
                return Response(status=200)
            else:
                logger.error(f"Avatar update form for user '{request.user.username}' is invalid. Errors: {form.errors}")
                return Response(status=400, data=form.errors)  # Возвращаем ошибки формы

        except Exception as e:
            logger.error(f"Error updating avatar for user '{request.user.username}': {str(e)}")
            return Response(status=500)


class ChangePasswordAPIView(APIView):
    """
        Представление для смены пароля пользователя в системе.
    """
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        try:
            user = request.user
            current_password = request.data.get('currentPassword')
            new_password = request.data.get('newPassword')

            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                logger.info(f"User '{request.user.username}' changed their password.")
                return Response(status=200)
            else:
                logger.warning(
                    f"Password change failed for user '{request.user.username}': incorrect current password.")
                return Response(status=500)
        except Exception as e:
            logger.error(f"Error changing password for user '{request.user.username}': {str(e)}")
            return Response(status=500)


