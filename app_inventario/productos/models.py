from django.db import models

class Usuario(models.Model):
    id_user = models.AutoField(primary_key=True)
    nom_user = models.CharField(max_length=20, unique=True)
    contrasena = models.CharField(max_length=50)
    rol = models.CharField(max_length=20)

    class Meta:
        db_table = 'usuarios'  
        managed = False       

    def __str__(self):
        return self.nom_user


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'categorias'
        managed = False

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=150)
    contacto_nombre = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'proveedores'
        managed = False

    def __str__(self):
        return self.nombre_empresa


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    codigo_barras = models.CharField(max_length=50, unique=True, blank=True, null=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, db_column='id_categoria', blank=True, null=True)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, db_column='id_proveedor', blank=True, null=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock_actual = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=5)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'productos'
        managed = False

    def __str__(self):
        return self.nombre


class HistorialInventario(models.Model):
    id_movimiento = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto')
    tipo_movimiento = models.CharField(max_length=10)
    cantidad = models.IntegerField()
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'historial_inventario'
        managed = False