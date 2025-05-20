from rest_framework import serializers
from .models import Cliente, Producto, Factura, DetalleFactura

# --- Cliente ---
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'rnc']

# --- Producto ---
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio']

# --- Detalle de Factura ---
class DetalleFacturaSerializer(serializers.ModelSerializer):
    factura = serializers.PrimaryKeyRelatedField(queryset=Factura.objects.all())
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
   # subtotal = producto.cantidad * producto.precio

    class Meta:
        model = DetalleFactura
        fields = ['id', 'factura', 'producto', 'cantidad', 'subtotal']

# --- Factura ---
class FacturaSerializer(serializers.ModelSerializer):
    productos = serializers.SerializerMethodField()
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())

    class Meta:
        model = Factura
        fields = ['id', 'cliente', 'fecha_emision', 'total', 'productos']
        read_only_fields = ['fecha_emision', 'total']

    def get_productos(self, obj):
        detalles = DetalleFactura.objects.filter(factura=obj)
        return DetalleFacturaSerializer(detalles, many=True).data

# --- Crear Factura ---
class FacturaCreateSerializer(serializers.ModelSerializer):
    productos = serializers.ListField(
        child=serializers.DictField(), write_only=True
    )

    class Meta:
        model = Factura
        fields = ['cliente', 'productos',]

    def create(self, validated_data):
        productos_data = validated_data.pop('productos')
        factura = Factura.objects.create(cliente=validated_data['cliente'], total=0)

        total = 0
        for item in productos_data:
            producto = Producto.objects.get(id=item['producto'])
            cantidad = item['cantidad']
            subtotal = cantidad * producto.precio

            DetalleFactura.objects.create(
                factura=factura,
                producto=producto,
                cantidad=cantidad,
                subtotal=subtotal
            )
            total += subtotal

        factura.total = total
        factura.save()
        return factura
