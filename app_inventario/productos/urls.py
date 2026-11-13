from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('almacen_dashboard/', views.almacen_dashboard, name='almacen_dashboard'),
    path('ventas_dashboard/', views.ventas_dashboard, name='ventas_dashboard'),
    
    path('obtener_producto_json/<int:id_producto>/', views.obtener_producto_json, name='obtener_producto_json'),
    
    path('registrar_movimiento_vendedor/', views.registrar_movimiento_vendedor, name='registrar_movimiento_vendedor'),
    path('guardar_usuario/', views.guardar_usuario, name='guardar_usuario'),
    path('eliminar_usuario/<int:id_user>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('guardar_categoria/', views.guardar_categoria, name='guardar_categoria'),
    path('eliminar_categoria/<int:id>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('guardar_proveedor/', views.guardar_proveedor, name='guardar_proveedor'),
    path('eliminar_proveedor/<int:id_proveedor>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('guardar_producto_almacen/', views.guardar_producto_almacen, name='guardar_producto_almacen'),
    path('eliminar_producto/<int:id_producto>/', views.eliminar_producto, name='eliminar_producto'),
]