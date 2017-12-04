from __future__ import unicode_literals

from django.shortcuts import render_to_response, HttpResponse, render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from cotizacion.models import * 
from django.contrib.auth.models import User
import json
import hashlib
import json
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta, time
from django.db.models import Q


class Index(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        personas_lista = Persona.objects.all()
        if request.user.is_authenticated: 
            return redirect('/cotizaciones')
        return render(
            request,
            self.template_name,
            {
                'personas_lista':personas_lista,
            }
        )

    def post(self, request, *args, **kwargs):
        logout(request)
        user = authenticate(username=request.POST["usuario"], password=request.POST["password"])
        fail = False
        if user:
            login(request, user)
            return redirect('/cotizaciones')
            
        else:
            fail = True
            return render(
                request,
                self.template_name,
                {
                    'fail': fail,
                }
            )


class Registro(TemplateView):
    template_name = "registro.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated: 
            return redirect('/cotizaciones')
        return render(
            request,
            self.template_name,
            {
                'request':request
            }
        )

    def post(self, request, *args, **kwargs):
        error = False
        if User.objects.filter(username=request.POST['user']).exists():
            error = 'Usuario Ya Existe'
            return render(
                request,
                self.template_name,
                {
                    'error':error
                }
            )
        else:
            user = User(
                username=request.POST['user'],
                first_name=request.POST['nombre'],
                last_name=request.POST['apellido'],
            )
            user.set_password(request.POST['password'])
            user.save()
            if Persona.objects.filter(cedula=request.POST['cedula']).exists():
                error = 'Persona ya registrada'
                return render(
                    request,
                    self.template_name,
                    {
                        'error':error
                    }
                )
            else:
                persona = Persona(
                    user=user,
                    cedula=request.POST['cedula'],
                )
                persona.save()
                login(request, user)
                return redirect('/cotizaciones')


class Cotizaciones(TemplateView):
    template_name = "cotizacion.html"

    def get(self, request, *args, **kwargs):
        producto_lista = Producto.objects.all()
        proveedor_lista = Proveedor.objects.all()
        cotizaciones_lista = []
        if request.user.is_staff:
            cotizaciones_lista = Cotizacion.objects.all()
        else:
            cotizaciones_lista = Cotizacion.objects.filter(user=request.user)
        return render(
            request,
            self.template_name,
            {
                'producto_lista':producto_lista,
                'cotizaciones_lista':cotizaciones_lista,
                'proveedor_lista':proveedor_lista,
            }
        )


def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect('/')


@csrf_exempt
def aceptar(request, *args, **kwargs):
    cotizacion = Cotizacion.objects.filter(id=request.POST['id']).update(
        proveedor_id=request.POST.get('proveedor', None),
        estado='A'
    )
    return redirect('/cotizaciones')


@csrf_exempt
def rechazar(request, *args, **kwargs):
    cotizacion = Cotizacion.objects.filter(id=request.POST['id']).update(
        estado='R'
    )
    return redirect('/cotizaciones')


def cotizaciones_json(request, *args, **kwargs):
    if request.user.is_staff:
        cotizaciones_lista = Cotizacion.objects.all()
    else:
        cotizaciones_lista = Cotizacion.objects.filter(user=request.user)
    dicc = {}
    lista = []
    for cotizacion in cotizaciones_lista:
        dicc = {
            'id': cotizacion.id,
            'producto':cotizacion.producto.nombre,
            'user':cotizacion.user.get_full_name(),
            'cantidad':cotizacion.cantidad,
            'fecha_creacion':cotizacion.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
            
            'estado':cotizacion.estado,
        }
        if cotizacion.proveedor:
            dicc['proveedor']={
                'nombre':cotizacion.proveedor.nombre,
                'telefono':cotizacion.proveedor.telefono,
                'direccion':cotizacion.proveedor.direccion,
            }
        if cotizacion.fecha_aprobacion:
            dicc['fecha_aprobacion']=cotizacion.fecha_aprobacion.strftime('%Y-%m-%d %H:%M:%S'),
        lista.append(dicc)
    result = json.dumps(lista, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json; charset=utf-8')


def proveedores_json(request, *args, **kwargs):
    proveedores_lista = Proveedor.objects.all()
    dicc = {}
    lista = []
    for proveedor in proveedores_lista:
        dicc={
            'id':proveedor.id,
            'nombre':proveedor.nombre,
            'telefono':proveedor.telefono,
            'direccion':proveedor.direccion,
        }
        lista.append(dicc)
    result = json.dumps(lista, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json; charset=utf-8')


@csrf_exempt
def nueva_cotizacion(request, *args, **kwargs):
    cotizacion = Cotizacion(
        producto_id=request.POST['producto'],
        user=request.user,
        proveedor_id=request.POST.get('proveedor', None),
        cantidad=request.POST['cantidad'],
    )
    if request.POST.get('proveedor', None) == None:
        cotizacion.estado='S'
    else:
        cotizacion.estado='A'
    cotizacion.save()
    return redirect('/cotizaciones')
