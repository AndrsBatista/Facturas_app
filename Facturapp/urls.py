from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, ProductoViewSet, FacturaViewSet, DetalleFacturaViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'facturas', FacturaViewSet)
router.register(r'detalles', DetalleFacturaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
