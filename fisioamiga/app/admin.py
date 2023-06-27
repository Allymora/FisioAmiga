from django.contrib import admin
from .models import Agenda, Terapia, CodigoConfirmacionHash

# Register your models here.
class AgendaAdmin(admin.ModelAdmin):
    list_display = [
        'dia', 'horario'
    ]

admin.site.register(Agenda)
admin.site.register(Terapia)
admin.site.register(CodigoConfirmacionHash)