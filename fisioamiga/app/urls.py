from django.contrib import admin 
from django.urls import path, include 
from django.conf.urls import handler404
from . import views

urlpatterns = [
path('', views.index, name='index'),
path('index/', views.index2, name='index2'),
path('login/', views.login_view, name='login'),
path('register/', views.register, name='register'),
path('logout/', views.logout_view, name="logout"),
path('register/<str:hash>/', views.confirmacion_correo, name="confirmacion_correo"),

#admin
path('app/', views.app, name="app"),
path('app/calendar', views.calendar, name="calendar"),
path('app/tables', views.tables, name="tables"),
path('app/terapia', views.terapias, name="terapia"),
path('app/terapiaAtualizar/<str:pk>', views.terapias_atualizar, name="terapia_actualizar"),
path('app/terapiaDelete/<str:pk>', views.terapia_delete, name="terapia_delete"),
path('app/Status', views.Status, name="Status"),
path('app/agenda_confirmacion/<str:pk>', views.confirmacion_agenda, name="confirmacion_agenda"),
path('confirmacion_asistencia/<str:hash>/', views.confirmacion_asistencia, name="confirmacion_asistencia"),
path('eliminar_asistencia/<str:hash>/', views.eliminar_asistencia, name="eliminar_asistencia"),

#cliente 
path('cliente/', views.cliente_app, name="cliente"),
path('cliente/lista', views.cliente_lista, name="cliente_lista"),

]
