from django.db import models


class ProveedorFarmacia(models.Model):
    nombre_proveedor = models.CharField(max_length=100)
    contacto_persona = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    direccion_proveedor = models.CharField(max_length=255)
    ruc = models.CharField(max_length=20)
    fecha_registro = models.DateField()

    def __str__(self):
        return self.nombre_proveedor


class Medicamento(models.Model):
    nombre_medicamento = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    proveedor = models.ForeignKey(ProveedorFarmacia, on_delete=models.CASCADE)
    fecha_vencimiento = models.DateField()
    codigo_barra = models.CharField(max_length=50)
    principio_activo = models.CharField(max_length=255)
    forma_farmaceutica = models.CharField(max_length=100)
    requiere_receta = models.BooleanField()

    def __str__(self):
        return self.nombre_medicamento


class ClienteFarmacia(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    direccion = models.CharField(max_length=255)
    fecha_registro = models.DateField()
    num_seguro_medico = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    preferencias = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Farmaceutico(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20)
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    licencia_colegiado = models.CharField(max_length=50)
    turno = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class RecetaMedica(models.Model):
    # Relación con Cliente
    cliente = models.ForeignKey(ClienteFarmacia, on_delete=models.CASCADE)

    # Relación con Médico/Veterinario (campo genérico, editable según implementación)
    id_medico_receto = models.IntegerField()

    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    diagnostico = models.TextField()
    medicamento_recetado_texto = models.TextField()
    dosis_indicada = models.TextField()
    estado_receta = models.CharField(max_length=50)

    def __str__(self):
        return f"Receta {self.id} - {self.cliente}"


class VentaFarmacia(models.Model):
    fecha_venta = models.DateTimeField()
    farmaceutico = models.ForeignKey(Farmaceutico, on_delete=models.CASCADE)
    cliente = models.ForeignKey(ClienteFarmacia, on_delete=models.CASCADE)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)
    descuento_total = models.DecimalField(max_digits=5, decimal_places=2)
    numero_factura = models.CharField(max_length=50)
    estado_venta = models.CharField(max_length=50)

    def __str__(self):
        return f"Venta {self.id} - {self.numero_factura}"


class DetalleVentaFarmacia(models.Model):
    venta = models.ForeignKey(VentaFarmacia, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario_venta = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva_aplicado = models.DecimalField(max_digits=5, decimal_places=2)
    receta_asociada = models.ForeignKey(RecetaMedica, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Detalle {self.id} de Venta {self.venta.id}"
