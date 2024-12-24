from rest_framework import routers
from .views import ProductView,CartView

router = routers.DefaultRouter()
router.register(r'products', ProductView, basename='products')
router.register(r'cart', CartView, basename='cart')

urlpatterns = router.urls
