from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = "Спасибо за заказ!"


class CanceledTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/canceled.html'


class OrderListView(TitleMixin, ListView):  # Отображение кнопки заказы
    template_name = 'orders/orders.html'
    title = 'Заказы'
    queryset = Order.objects.all()
    ordering = ('-created',)

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):  # Для определения номера заказа
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f"Store - Заказ #{self.object.id}"
        return context


class OrderCreateView(TitleMixin, CreateView):
    title = "Оформление заказа"
    template_name = 'orders/order-create.html'
    form_class = OrderForm  # Для класса CreateView - это обязательный параметр
    success_url = reverse_lazy('orders:order_create')

    def post(self, request, *args, **kwargs):  # Создание объекта (Stripe)
        super(OrderCreateView, self).post(self, request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)

        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)  # SEE_OTHER == 303

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)

    # Метод form_valid - это метод в классе CreateView из библиотеки Django,
    # который вызывается после успешной валидации формы. В этом методе вы
    # можете выполнять дополнительные действия с данными формы перед
    # сохранением их в базу данных. В данном случае, когда форма оформления
    # заказа проходит валидацию, метод form_valid устанавливает пользователя
    # (initiator) заказа в текущего пользователя (self.request.user).
    # После этого вызывается метод form_valid родительского класса
    # (super(OrderCreateView, self).form_valid(form)), который сохраняет
    # данные формы в базу данных и выполняет стандартное поведение для
    # успешного завершения создания объекта.


# Stripe webhook
@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']  # ['id']
        fulfill_order(session)

    return HttpResponse(status=200)


def fulfill_order(session):  # Обновление корзины после оплаты товаров
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
