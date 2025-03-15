from django.contrib import admin

from products.models import Basket, Product, ProductCategory

admin.site.register(ProductCategory)


@admin.register(Product)  # Указание модели, с которой будет работать этот класс
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')  # Как мы хотим видеть продукты
    # Отображение самих продуктов/категорий
    fields = ('image', 'name', 'description', ('price', 'quantity'), 'stripe_product_price_id', 'category')
    readonly_fields = ('description',)
    search_fields = ('name',)  # Поле, по которому будет идти поиск
    ordering = ('price',)  # Сортировка


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0  # Доп поля в админ корзине
