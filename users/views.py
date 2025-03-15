from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin
from products.models import Basket
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import User

# Все модели и формы написал, но подключить их не получается, не знаю почему. EngineerSpock "Курс по Django" - №7-8


# CBV (Class Based Views) method
class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = "Store - Authorization"


# Миксины - класс с методами для доп обработок внутри других классов
class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')  # Переотправление юзера после успешного сохранения формы
    success_message = "You have successfully registered!"  # Не работает(
    title = "Store - Registration"


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = "Store - Personal account"

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

# FAILURE with EmailVerification
# class EmailVerificationView(TitleMixin, TemplateView):
#     title = "Store - Подтверждение электронной почты"
#     template_name = 'users/email_verification.html'
#
#     def get(self, request, *args, **kwargs):
#         code = kwargs['code']
#         user = User.objects.get(email=kwargs['email'])
#         email_verifications = EmailVerification.objects.filter(user=user, code=code)
#         if email_verifications.exists() and not email_verifications.first().is_expired():
#             user.is_verified_email = True
#             user.save()
#             return super(EmailVerificationView, self).get(request, *args, **kwargs)
#         else:
#             return HttpResponseRedirect(reverse('index'))

# FBV (Function Based Views) method
# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)  # Регистрация
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)  # Проверка, существует ли такой user
#             if user:
#                 auth.login(request, user)  # Авторизация пользователя
#                 return HttpResponseRedirect(reverse('index'))
#                 # Перенаправление на главную стр, reverse('index') - указывает на эту стр.
#                 # Ф-я reverse() возвращает строку адреса по названию из urls
#     else:
#         form = UserLoginForm()
#     context = {'form': form}
#     return render(request, 'users/login.html', context)

# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegistrationForm()
#     context = {'form': form}
#     return render(request, 'users/registration.html', context)


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "You have successfully registered")
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     context = {
#         'title': "Store - Профиль",
#         'form': form,
#         'baskets': Basket.objects.filter(user=request.user),
#         # filter(...) нужен для того, чтобы у каждого пользователя была своя корзина, а не общая
#     }
#     return render(request, 'users/profile.html', context)


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))
