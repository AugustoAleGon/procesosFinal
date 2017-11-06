from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# Registro de personas que solicita la cotización
class Persona(models.Model):
    cedula = models.IntegerField(unique=True)
    user =  models.OneToOneField(
        User,
        on_delete= models.CASCADE,
    )
    
    class Meta:
        verbose_name_plural = "Personas"

    def __unicode__(self):              # __unicode__ on Python 2
        return "%s %s" % (self.user.get_full_name(), self.cedula)
    
    def __str__(self):              # __unicode__ on Python 2
        return "%s %s" % (self.user.get_full_name(), self.cedula)


# Registro de proveedores al aceptar la cotización
class Proveedor(models.Model):
    nombre = models.CharField(max_length=30)
    telefono = models.CharField(max_length=30)
    direccion = models.CharField(max_length=150)
    
    class Meta:
        verbose_name_plural = "Proveedores"

    def __unicode__(self):              # __unicode__ on Python 2
        return self.nombre

    def __str__(self):              # __unicode__ on Python 2
        return self.nombre


# Producto solicitado
class Producto(models.Model):
    nombre = models.CharField(max_length=30)
    
    def __unicode__(self):              # __unicode__ on Python 2
        return self.nombre
    
    def __str__(self):              # __unicode__ on Python 2
        return self.nombre


# Registro de la cotización
class Cotizacion(models.Model):
    unidad_choices=(("U" , "Unidad"),("M" , "Metro"),("L" , "Litro"))
    estado_choices=(("S" , "Solicitud"),("A" , "Aprobado"),("R" , "Rechazado"))
    unidad = models.CharField(max_length=1, choices=unidad_choices)
    proveedor = models.ForeignKey(Proveedor, null=True, blank=True)
    producto = models.ForeignKey(Producto)
    user = models.ForeignKey(User)
    cantidad = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=1, choices=estado_choices)
    
    class Meta:
        verbose_name_plural = "Cotizaciones"

    def __unicode__(self):              # __unicode__ on Python 2
        return "proveedor: %s, producto: %s, solicitante: %s" % (self.proveedor, self.producto, self.user)
    
    def __str__(self):              # __unicode__ on Python 2
        return "proveedor: %s, producto: %s, solicitante: %s" % (self.proveedor, self.producto, self.user)
