from django.contrib.auth.models import AbstractUser
from django.db import models


# Расширение модели пользователя
class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)

# FAILURE with EmailVerification
# class EmailVerification(models.Model):
#     code = models.UUIDField(unique=True)  # Генерация уникальной ссылки для подт-ия почты юзера
#     user = models.ForeignKey(to=User, on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#     expiration = models.DateTimeField()  # Срок действия ссылки
#
#     def __str__(self):
#         return f"EmailVerification for {self.user.email}"
#
#     def send_verification_email(self):
#         link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
#         verification_link = f"{settings.DOMAIN_NAME}{link}"
#         subject = f"Подтверждение учётной записи для {self.user.username}"
#         message = "Для подтверждения учётной записи для {} перейдите по ссылке: {}".format(
#             self.user.email,
#             verification_link
#         )
#         send_mail(
#             subject=subject,
#             message=message,
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[self.user.email],
#             fail_silently=False,
#         )
#
#     def is_expired(self):
#         return True if now() >= self.expiration else False
