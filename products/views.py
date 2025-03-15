from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory


# CBV (Class Based Method) method
class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = "Goodman's store"


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Catalog'

    def get_queryset(self):  # Фильтрация по категориям (одежда, обувь...)
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):  # Отображение товаров
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context


@login_required  # Декоратор, который активирует контроллер только с зареганным юзером
def basket_add(request, product_id):  # Контроллер обработчик событий - добавление товаров в корзину
    Basket.create_or_update(product_id, request.user)
    # Возвращение пользователя на ту стр, на которой он добавил товар в корзину (каталог/корзина)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

# FBV (Function Based Views) - контроллер вида функции
# def index(request):
#     context = {'title': "Goodman's store"}
#     return render(request, 'products/index.html', context)

# def products(request, category_id=None, page_number=1):  # None нужен, чтобы указать, категория не всегда мб выбрана
#     # Способ через if
#     # if category_id:
#     #     products = Product.objects.filter(category_id=category_id)
#     # else:
#     #     products = Product.objects.all()
#
#     # Способ через тернарный оператор
#     products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
#
#     per_page = 3  # Кол-во товаров на странице
#     paginator = Paginator(products, per_page)  # Переход между страницами
#     products_paginator = paginator.page(page_number)
#
#     context = {
#         'title': "Catalog",
#         'categories': ProductCategory.objects.all(),
#         'products': products_paginator
#     }
#     return render(request, 'products/products.html', context)
