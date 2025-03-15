from django.urls import path

from products.views import ProductsListView, basket_add, basket_remove

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('category/<int:category_id>/', ProductsListView.as_view(), name='category'),
    path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),
    # FBV method
    # path('', products, name='index'),
    # path('category/<int:category_id>/', products, name='category'),  # Фильтрация по категориям
    # path('page/<int:page_number>/', products, name='paginator'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),  # ../products/baskets/add/<product_id>/
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove')
    # ../products/baskets/remove/<basket_id>/
]
