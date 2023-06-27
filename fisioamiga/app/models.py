from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.fields.related import ForeignKey
from datetime import date
# Create your models here.
NAME_TERAPIA = (
        ("Tratamiento rehabilitador de la parálisis facial", "Tratamiento rehabilitador de la parálisis facial"),
        ("Terapia Manual Osteopática", "Terapia Manual Osteopática"),
        ("Fisioterapia Deportiva", "Fisioterapia Deportiva"),
        ("Terapia Manual Osteopática", "Terapia Manual Osteopática"),
        ("Fisioterapia en el tratamiento del dolor de rodilla", "Fisioterapia en el tratamiento del dolor de rodilla"),
        ("Fisioterapia en tendinopatías", "Fisioterapia en tendinopatías"),
    )

class Terapia(models.Model):
    name =  models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.name}'

def validar_dia(value):
    today = date.today()
    weekday = date.fromisoformat(f'{value}').weekday()

    if value < today:
        raise ValidationError('No es posible elegir una fecha tardía.')
    if (weekday == 5) or (weekday == 6):
        raise ValidationError('Elija un día laborable de la semana.')

HORARIOS = (
        ("1", "10:00 a 11:30"),
        ("2", "1:00  a 2:00"),
        ("3", "2:00  a 3:30"),
        ("4", "3:30  a 5:00"),
    )
class Agenda(models.Model):
    dia = models.DateField(help_text="Agendar dia", validators=[validar_dia])
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    horario = models.CharField(max_length=10, choices=HORARIOS)
    terapia = models.ForeignKey(Terapia, on_delete=models.CASCADE, null=True)
    activa = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.dia.strftime("%b %d %Y")} - {self.get_horario_display()}'

STATUS = (
        ("Aceptado", "Aceptado"),
        ("Pendiente", "Pendiente"),
        ("Cancelado", "Cancelado"),

)

class CodigoConfirmacionHash(models.Model):
    name =  models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    agenda  = models.ForeignKey(Agenda, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user} - {self.name} - {self.status}'
