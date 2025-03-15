from django.urls import include, path
from rest_framework import routers

from api.views import BasketModelViewSet, ProductModelViewSet

app_name = 'api'

# Добавление всех методов (GET, POST, PUT и т. д.) в API
router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'baskets', BasketModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
