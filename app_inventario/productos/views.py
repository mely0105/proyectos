from django.db import models, IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Usuario, Producto, Categoria, Proveedor, HistorialInventario


# --- API JSON PARA AUTO-COMPLETAR DATOS POR ID ---
def obtener_producto_json(request, id_producto):
    try:
        producto = Producto.objects.get(pk=id_producto)
        data = {
            'success': True,
            'nombre': producto.nombre,
            'codigo_barras': producto.codigo_barras or '',
            'id_categoria': producto.id_categoria.id_categoria if producto.id_categoria else '',
            'id_proveedor': producto.id_proveedor.id_proveedor if producto.id_proveedor else '',
            'descripcion': producto.descripcion or '',
            'precio_compra': float(producto.precio_compra),
            'precio_venta': float(producto.precio_venta),
        }
    except Producto.DoesNotExist:
        data = {'success': False}
    return JsonResponse(data)


# --- AUTENTICACIÓN Y REDIRECCIÓN ---
def index_view(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    rol = request.session.get('rol')
    if rol == 'administrador':
        return redirect('admin_dashboard')
    elif rol == 'almacenista':
        return redirect('almacen_dashboard')
    elif rol == 'vendedor':
        return redirect('ventas_dashboard')
    else:
        return redirect('login')


def login_view(request):
    if 'usuario_id' in request.session:
        return redirect('index')

    if request.method == 'POST':
        user_input = request.POST.get('username') or request.POST.get('Nombre de usuario')
        pass_input = request.POST.get('password') or request.POST.get('contraseña')

        try:
            usuario_db = Usuario.objects.get(nom_user=user_input, contrasena=pass_input)
            request.session['usuario_id'] = usuario_db.id_user
            request.session['nom_user'] = usuario_db.nom_user
            request.session['rol'] = usuario_db.rol
            return redirect('index')
        except Usuario.DoesNotExist:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')


# --- DASHBOARDS ---
def admin_dashboard(request):
    if request.session.get('rol') != 'administrador':
        return redirect('index')
    
    productos = Producto.objects.all().order_by('-id_producto')
    
    try:
        productos_stock_bajo = Producto.objects.filter(stock_actual__lte=models.F('stock_minimo'))
    except Exception:
        productos_stock_bajo = []

    contexto = {
        'usuarios': Usuario.objects.all(),
        'productos': productos,
        'proveedores': Proveedor.objects.all(),
        'categorias': Categoria.objects.all(),
        'historial': HistorialInventario.objects.select_related('id_producto').all().order_by('-fecha_movimiento')[:15],
        'productos_stock_bajo': productos_stock_bajo,
    }
    return render(request, 'admin_dashboard.html', contexto)


def almacen_dashboard(request):
    if request.session.get('rol') not in ['administrador', 'almacenista']:
        return redirect('index')
    
    productos = Producto.objects.all().order_by('-id_producto')
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()
    
    try:
        productos_stock_bajo = Producto.objects.filter(stock_actual__lte=models.F('stock_minimo'))
    except Exception:
        productos_stock_bajo = []

    contexto = {
        'productos': productos,
        'categorias': categorias,
        'proveedores': proveedores,
        'productos_stock_bajo': productos_stock_bajo
    }
    return render(request, 'almacen_dashboard.html', contexto)


def ventas_dashboard(request):
    if request.session.get('rol') not in ['administrador', 'vendedor']:
        return redirect('index')
    
    productos = Producto.objects.all().order_by('-id_producto')
    return render(request, 'ventas_dashboard.html', {'productos': productos})


# --- OPERACIONES DE PRODUCTOS Y MOVIMIENTOS ---
def guardar_producto_almacen(request):
    if request.method == 'POST':
        id_producto = request.POST.get('id_producto')
        nombre = request.POST.get('nombre')
        codigo_barras = request.POST.get('codigo_barras')
        id_categoria = request.POST.get('id_categoria')
        id_proveedor = request.POST.get('id_proveedor')
        descripcion = request.POST.get('descripcion')
        tipo_mov = request.POST.get('tipo_movimiento', 'ENTRADA')
        stok = int(request.POST.get('stok', 0))
        precio_compra = request.POST.get('precio_compra')
        precio_venta = request.POST.get('precio_venta')
        motivo = request.POST.get('motivo')

        categoria_obj = None
        if id_categoria:
            categoria_obj = Categoria.objects.filter(pk=id_categoria).first()

        proveedor_obj = None
        if id_proveedor:
            proveedor_obj = Proveedor.objects.filter(pk=id_proveedor).first()

        if id_producto:  # EDITAR EXISTENTE
            producto = get_object_or_404(Producto, pk=id_producto)
            producto.nombre = nombre
            producto.codigo_barras = codigo_barras
            producto.id_categoria = categoria_obj
            producto.id_proveedor = proveedor_obj
            producto.descripcion = descripcion
            producto.precio_compra = precio_compra
            producto.precio_venta = precio_venta
            
            if tipo_mov == 'ENTRADA':
                producto.stock_actual += stok
            elif tipo_mov == 'AJUSTE':
                producto.stock_actual = stok
            
            producto.save()

            HistorialInventario.objects.create(
                id_producto=producto,
                tipo_movimiento=tipo_mov,
                cantidad=stok,
                motivo=motivo or f'Movimiento {tipo_mov} registrado'
            )
            messages.success(request, f"Producto '{producto.nombre}' actualizado correctamente.")

        else:  # NUEVO PRODUCTO
            nuevo_p = Producto.objects.create(
                nombre=nombre,
                codigo_barras=codigo_barras,
                id_categoria=categoria_obj,
                id_proveedor=proveedor_obj,
                descripcion=descripcion,
                stock_actual=stok,
                precio_compra=precio_compra,
                precio_venta=precio_venta
            )

            HistorialInventario.objects.create(
                id_producto=nuevo_p,
                tipo_movimiento='ENTRADA',
                cantidad=stok,
                motivo=motivo or 'Creación inicial de producto'
            )
            messages.success(request, f"Producto '{nuevo_p.nombre}' creado con éxito.")

    rol = request.session.get('rol')
    if rol == 'administrador':
        return redirect('admin_dashboard')
    elif rol == 'almacenista':
        return redirect('almacen_dashboard')
    return redirect('login')


def registrar_movimiento_vendedor(request):
    if request.session.get('rol') not in ['administrador', 'vendedor']:
        return redirect('index')

    if request.method == 'POST':
        id_producto = request.POST.get('id_producto')
        tipo_movimiento = request.POST.get('tipo_movimiento')
        cantidad = int(request.POST.get('cantidad', 1))
        motivo = request.POST.get('motivo', '')

        producto = get_object_or_404(Producto, pk=id_producto)

        if tipo_movimiento == 'SALIDA':
            if producto.stock_actual >= cantidad:
                producto.stock_actual -= cantidad
                producto.save()

                HistorialInventario.objects.create(
                    id_producto=producto,
                    tipo_movimiento='SALIDA',
                    cantidad=cantidad,
                    motivo=motivo or 'Venta de producto'
                )
                messages.success(request, f"Salida/Venta registrada para {producto.nombre}. Quedan {producto.stock_actual} unidades.")
            else:
                messages.error(request, f"Stock insuficiente. Stock actual disponible: {producto.stock_actual}.")

        elif tipo_movimiento == 'AJUSTE':  # DEVOLUCIÓN: Se suma al stock actual
            producto.stock_actual += cantidad
            producto.save()

            HistorialInventario.objects.create(
                id_producto=producto,
                tipo_movimiento='ENTRADA',  # O 'AJUSTE' según prefieras en tu historial
                cantidad=cantidad,
                motivo=motivo or 'Devolución de cliente'
            )
            messages.success(request, f"Devolución/Ajuste registrado para {producto.nombre}. Stock actualizado: {producto.stock_actual}.")

    return redirect('ventas_dashboard')


# --- OPERACIONES USUARIOS / CATEGORÍAS / PROVEEDORES ---
def guardar_usuario(request):
    if request.session.get('rol') != 'administrador':
        return redirect('index')
    
    if request.method == 'POST':
        user_id = request.POST.get('id_user')
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')
        rol = request.POST.get('rol')

        if user_id:
            usr = get_object_or_404(Usuario, pk=user_id)
            usr.nom_user = usuario
            if password:
                usr.contrasena = password
            usr.rol = rol
            usr.save()
        else:
            Usuario.objects.create(nom_user=usuario, contrasena=password, rol=rol)

    return redirect('admin_dashboard')


def eliminar_usuario(request, id_user):
    if request.session.get('rol') != 'administrador':
        return redirect('index')
    usr = get_object_or_404(Usuario, pk=id_user)
    usr.delete()
    return redirect('admin_dashboard')


def guardar_categoria(request):
    if request.session.get('rol') != 'administrador':
        return redirect('index')
    
    if request.method == 'POST':
        cat_id = request.POST.get('id_categoria')
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        if cat_id:
            cat = get_object_or_404(Categoria, pk=cat_id)
            cat.nombre = nombre
            cat.descripcion = descripcion
            cat.save()
            messages.success(request, f"Categoría '{nombre}' actualizada correctamente.")
        else:
            try:
                Categoria.objects.create(nombre=nombre, descripcion=descripcion)
                messages.success(request, f"Categoría '{nombre}' agregada con éxito.")
            except IntegrityError:
                messages.error(request, f"La categoría '{nombre}' ya existe. Por favor ingresa un nombre diferente.")

    return redirect('admin_dashboard')


def eliminar_categoria(request, id):
    if request.session.get('rol') != 'administrador':
        return redirect('index')
    cat = get_object_or_404(Categoria, pk=id)
    cat.delete()
    return redirect('admin_dashboard')


def guardar_proveedor(request):
    if request.session.get('rol') != 'administrador':
        return redirect('index')
    
    if request.method == 'POST':
        prov_id = request.POST.get('id_proveedor')
        empresa = request.POST.get('empresa')
        contacto_nombre = request.POST.get('contacto_nombre')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')

        if prov_id:
            prov = get_object_or_404(Proveedor, pk=prov_id)
            prov.nombre_empresa = empresa
            prov.contacto_nombre = contacto_nombre
            prov.telefono = telefono
            prov.email = email
            prov.direccion = direccion
            prov.save()
        else:
            Proveedor.objects.create(
                nombre_empresa=empresa,
                contacto_nombre=contacto_nombre,
                telefono=telefono,
                email=email,
                direccion=direccion
            )

    return redirect('admin_dashboard')


def eliminar_proveedor(request, id_proveedor):
    if request.session.get('rol') != 'administrador':
        return redirect('index')
    prov = get_object_or_404(Proveedor, pk=id_proveedor)
    prov.delete()
    return redirect('admin_dashboard')


def eliminar_producto(request, id_producto):
    if request.session.get('rol') != 'administrador':
        return redirect('index')
    prod = get_object_or_404(Producto, pk=id_producto)
    prod.delete()
    return redirect('admin_dashboard')