from rest_framework import viewsets
from django.shortcuts import render
from django.http import JsonResponse
from .models import Cliente, Producto, Factura, DetalleFactura
from .serializers import (
    ClienteSerializer,
    ProductoSerializer,
    FacturaSerializer,
    FacturaCreateSerializer,
    DetalleFacturaSerializer
)

def home(request):
    return render(request, 'index.html')

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class DetalleFacturaViewSet(viewsets.ModelViewSet):
    queryset = DetalleFactura.objects.all()
    serializer_class = DetalleFacturaSerializer

class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return FacturaCreateSerializer
        return FacturaSerializer
