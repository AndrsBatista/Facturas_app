from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, ProductoViewSet, FacturaViewSet, DetalleFacturaViewSet, home, registrar_cliente, registrar_producto, registrar_factura, ver_facturas, generar_pdf_factura
from .views import CustomAuthToken

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'facturas', FacturaViewSet)
router.register(r'detalles', DetalleFacturaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('cliente/', registrar_cliente, name='cliente'),
    path('producto/', registrar_producto, name='producto'),
    path('factura/', registrar_factura, name='factura'),
    path('ver-facturas/', ver_facturas, name='ver_facturas'),
    path('factura/<int:factura_id>/', generar_pdf_factura, name='factura_pdf'),
]
