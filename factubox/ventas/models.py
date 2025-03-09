
from django.db import models
from inventario.models import Producto


# clase venta con su campo de fecha
class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(
        max_length=20,
        choices=[('Efectivo', 'Efectivo'), ('QR', 'QR'), ('Tarjeta', 'Tarjeta')]
    )
    
    descuento = models.DecimalField(
        max_digits=5, decimal_places=2, default=0,
        help_text="Descuento en porcentaje (ej. 10 para 10%)"
    )
    descripcion_descuento = models.TextField(
        blank=True, null=True,
        help_text="Motivo del descuento"
    )
    
    def __str__(self):
        return f"Venta {self.id} - {self.fecha}"

# calse detalleVenta con sus campos
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) 
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Solo descontamos stock al crear un nuevo registro
        if self.pk is None:
            self.producto.cantidad -= self.cantidad
            self.producto.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"