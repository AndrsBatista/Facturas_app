from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    rnc = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    productos = models.ManyToManyField(Producto, through='DetalleFactura')

    def __str__(self):
        return f"Factura {self.id} - {self.cliente.nombre}"

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Calcular el subtotal como cantidad x precio del producto
        self.subtotal = self.cantidad * self.producto.precio
        super(DetalleFactura, self).save(*args, **kwargs)


    def __str__(self):
        return f"Detalle Factura {self.factura.id} - Producto {self.producto.nombre}"

