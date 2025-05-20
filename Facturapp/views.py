from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Cliente, Producto, Factura, DetalleFactura
from .serializers import (
    ClienteSerializer,
    ProductoSerializer,
    FacturaSerializer,
    FacturaCreateSerializer,
    DetalleFacturaSerializer
)
from django.utils.timezone import now
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from .forms import LoginForm

@login_required
def home(request):
    return render(request, 'index.html')

@login_required
def cliente_view(request):
    return render(request, 'cliente.html')

@login_required
def producto_view(request):
    return render(request, 'producto.html')

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
    

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Cliente

@login_required
def registrar_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        rnc = request.POST.get('rnc')

        #Validación RNC
        if not rnc.isdigit() or len(rnc) != 11:
            return render(request, 'cliente.html', {
                'error': 'El RNC debe contener exactamente 11 dígitos numéricos.',
                'nombre': nombre,
                'rnc': rnc
            })
        

        # Verificar si el RNC ya existe
        if Cliente.objects.filter(rnc=rnc).exists():
            return render(request, 'cliente.html', {
                'error': 'Ya existe un cliente con este RNC. Por favor, ingrese otro.',
                'nombre': nombre,
                'rnc': rnc
            })
        Cliente.objects.create(nombre=nombre, rnc=rnc)
        return redirect('factura')

    return render(request, 'cliente.html')

@login_required
def registrar_producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        Producto.objects.create(nombre=nombre, descripcion=descripcion, precio=precio)
        return redirect('home')
    return render(request, 'producto.html')

@login_required
def registrar_factura(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        cliente_rnc = request.POST.get('rnc')
        productos_ids = request.POST.getlist('productos[]')
        cantidades = request.POST.getlist('cantidades[]')

        cliente = Cliente.objects.get(id=cliente_id)
        total = Decimal('0.00') 
        factura = Factura.objects.create(cliente=cliente, fecha_emision=now().date(), total=0)

        cantidades = [Decimal(cantidad) for cantidad in cantidades]

        for prod_id, cantidad in zip(productos_ids, cantidades):
            producto = Producto.objects.get(id=prod_id)
            subtotal = producto.precio * cantidad
            total += subtotal
            factura.detallefactura_set.create(producto=producto, cantidad=cantidad)

        factura.total = total
        factura.save()
        return redirect('home')

    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    return render(request, 'factura.html', {
        'clientes': clientes,
        'productos': productos
    })

@login_required
def ver_facturas(request):
    facturas = Factura.objects.all().prefetch_related('detallefactura_set', 'cliente')

    for factura in facturas:
        total_productos = sum(detalle.cantidad for detalle in factura.detallefactura_set.all())
        factura.cantidad_productos = total_productos

    return render(request, 'ver_facturas.html', {'facturas': facturas})

#LOGIN
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def login_view(request):
    form = LoginForm(request.POST or None)
    error = None

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = "Credenciales incorrectas"

    return render(request, 'login.html', {'form': form, 'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        })
    
#EXPORTACIÓN A PDF
from django.template.loader import get_template
from xhtml2pdf import pisa #NOTA: "Pisa" se encarga de convertir HTML a PDF

def generar_pdf_factura(request, factura_id):
    factura = Factura.objects.get(id=factura_id)
    template = get_template('pdf_factura.html')
    html = template.render({'factura': factura})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{factura_id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status=500)
    return response
