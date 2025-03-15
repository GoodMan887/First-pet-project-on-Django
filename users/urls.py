from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import UserLoginView, UserProfileView, UserRegistrationView

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    # <int:pk> нужен, чтобы Django понял с каким именно объектом (юзером) надо работать, pk - primary key
    path('logout/', LogoutView.as_view(), name='logout'),
    # FAILURE with EmailVerification
    # path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
]

# FBV
# urlpatterns = [
#     path('login/', login, name='login'),
#     path('registration/', registration, name='registration'),
#     path('profile/', profile, name='profile'),
#     path('logout/', logout, name='logout'),
# ]
