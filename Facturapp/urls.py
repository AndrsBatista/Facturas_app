from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  home, registrar_cliente, registrar_producto, registrar_factura, ver_facturas, generar_pdf_factura, usuario_dashboard, admin_dashboard, crear_usuario, editar_usuario, usuario_list, borrar_usuario, producto_list, borrar_producto, editar_producto
from .views import CustomAuthToken

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('usuario-dashboard/', usuario_dashboard, name='usuario_dashboard'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('cliente/', registrar_cliente, name='cliente'),
    path('producto/', producto_list, name='producto'),
    path('factura/', registrar_factura, name='factura'),
    path('ver-facturas/', ver_facturas, name='ver_facturas'),
    path('factura/<int:factura_id>/', generar_pdf_factura, name='factura_pdf'),
    path('crear-usuario/', crear_usuario, name='crear_usuario'),
    path('editar-usuario/<int:user_id>/', editar_usuario, name='editar_usuario'),
    path('borrar-usuario/<int:user_id>/', borrar_usuario, name='borrar_usuario'),
    path('usuarios/', usuario_list, name='usuario_list'),
    path('borrar-producto/<int:producto_id>/', borrar_producto, name='borrar_producto'),
    path('editar-producto/<int:producto_id>/', editar_producto, name='editar_producto'),
    path('registrar-producto/', registrar_producto, name='registrar_producto'),
    path('', home, name='home'),
]
