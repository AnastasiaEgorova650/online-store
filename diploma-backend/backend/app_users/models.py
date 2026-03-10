from django.contrib.auth.models import User
from django.db import models


def avatar_image_directory_path(instance: "UserProfile", filename: str) -> str:
    return f"profile/user_{instance.pk}/avatar/{filename}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Имя")
    surname = models.CharField(max_length=200, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=200, verbose_name="Отчество")
    phone = models.CharField(max_length=15, verbose_name="Номер телефона")
    email = models.EmailField(max_length=200, verbose_name="Email")
    avatar = models.ImageField(
        null=True, blank=True, upload_to=avatar_image_directory_path
    )


    def get_avatar(self):
        avatar = {
            "src": self.avatar.url,
            "alt": self.avatar.name,
        }
        return avatar


    def __str__(self):
        return self.name
