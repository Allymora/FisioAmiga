from django.shortcuts import get_object_or_404, render, redirect   
from django.http import HttpResponseNotFound, HttpResponse
from django.contrib import messages
from .models import *
from django.db.models import Q
#date
from datetime import date, datetime

# AUTH
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required

#Email
from django.conf import settings 
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives, send_mail
from werkzeug.security import generate_password_hash

#forms
from .form import AgendaDiaForm, TerapiaForm


def index(request):
   # logout(request)
   return render(request, 'index.html')
   
@login_required(login_url='login')
def index2(request):
   user = User.objects.filter(username=request.user)[0]
   if user.is_superuser:
      return render(request, 'admin_viev/confirmacion.html')
   else:
      return redirect('index')

@login_required(login_url='login')
@permission_required('user.is_superuser')
def calendar(request):
   return render(request, 'admin_viev/pages-calendar.html')

@login_required(login_url='login')
@permission_required('user.is_superuser')
def tables(request):
   object_list = Agenda.objects.filter().exclude(activa=True).order_by('dia')
   context = {
      "object_list":object_list,
   }
   return render(request, 'admin_viev/tables.html',context)

@login_required(login_url='login')
@permission_required('user.is_superuser')
def terapias(request):
   page = "terapias"
   form = TerapiaForm(request.POST or None)
   if request.method == "POST":
         if form.is_valid():
            form.save()
            return redirect('terapia')
         else:
            return HttpResponse("405")      
   else:
      terapia_object = Terapia.objects.all()
      context = {'form': form,
                  'terapia_object': terapia_object,
                  'page': page,
      }
      return render(request, 'admin_viev/terapia.html', context)

@login_required(login_url='login')
@permission_required('user.is_superuser')
def terapias_atualizar(request, pk):
   page = "actualizar"
   try:
      terapia_object = Terapia.objects.get(id=pk)
   except:
      return HttpResponseNotFound("Not found")

   if request.method == "POST":
         form = TerapiaForm(request.POST,  instance=terapia_object)
         if form.is_valid():
            form.save()
            return redirect('terapia')
         else:
            return HttpResponse("405")      
   else:
      form = TerapiaForm(instance=terapia_object)
      terapia_object2 = Terapia.objects.all().exclude(id=pk)
      context = {'form': form,
                  'terapia_object': terapia_object2,
                  'page': page,
                  'id': pk
      }
      return render(request, 'admin_viev/terapia.html', context)

@login_required(login_url='login')
@permission_required('user.is_superuser')
def terapia_delete(request, pk):
   terapia = Terapia.objects.filter(id=pk)
   terapia.delete()
   return redirect("terapia")

@login_required(login_url='login')
@permission_required('user.is_superuser')
def Status(request):
   if request.method == 'POST':
      pass
   else:
      user_hash = CodigoConfirmacionHash.objects.all()
      context = { 
         "user_hash": user_hash
      }
      return render(request, 'admin_viev/confirmacion.html', context)

@login_required(login_url='login')
@permission_required('user.is_superuser')
def confirmacion_agenda(request, pk):
   userxd = Agenda.objects.get(id=pk)
   user = User.objects.get(id = userxd.user.id)
   if request.method == 'POST':
      cifrado = generate_password_hash(userxd.user.username)
      cifrado = cifrado[15:]
      confirmar = "agenda"
      user = CodigoConfirmacionHash.objects.create( name=cifrado, status="Pendiente", user=user, agenda=userxd)
      send_mail(userxd.user.email, userxd.user, cifrado, confirmar)  
      userxd.activa = True
      userxd.save()
      return redirect("tables")
   else:
      return render(request, 'admin_viev/tables.html')



@login_required(login_url='login')
@permission_required('user.is_superuser')
def app(request):
   if request.method == 'POST':
      pass
   else:
      return render(request, 'admin_viev/layout.html')

def login_view(request):
   logout(request)
   page = 'Login'
   context = {'page': page}
   if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']
      if username == '' or password == '':
         messages.error(request, 'Introduzca datos')
         return redirect(to='login')
      
      user = authenticate(username=username, password=password)
      if user is not None:
         login(request, user)
               
               
         return redirect(to='index2')
      else:
         messages.success(request, 'Activa tu correo o ingrese correctamente sus credenciales')
         return redirect(to='login')

   return render(request, 'loginAndRegister.html', context)


# valleally04@gmail.com

def register(request):
   page = 'Register'
   context = {'page': page}
   if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']
      password2 = request.POST['password2']
      email = request.POST['email']
      if password == password2:
         if User.objects.filter(username=username).exists():
               messages.success(
                  request, 'Datos incorrectos o usuario registrado')
               return redirect(to="register")
         elif User.objects.filter(email=email).exists():
            messages.success(
               request, 'Datos incorrectos o usuario registrado')
            return redirect(to="register")
         else:
            cifrado = generate_password_hash(username)
            cifrado = cifrado[15:]
            confirmar = "cuenta"
            send_mail(email, username, cifrado, confirmar)

            user = User.objects.create_user(
               username=username, password=password, email=email, first_name=cifrado, last_name= "cliente", is_active=False)
            messages.success(request, 'Se ha creado el usuario de forma satisfactoria, confirme su correo electronico')

            
            return redirect(to='login')
   else:
      return render(request, 'loginAndRegister.html', context)

@login_required(login_url='login')
def logout_view(request):
   logout(request)
   return redirect('login')

def send_mail(mail, username, cifrado, confirmar):
   if confirmar == "cuenta":
      texto = "Confirmar Cuenta  haz clic en el boton de abajo"
      agendado = "Es hora de confirmar cuenta"
      url = "register"
      url2 = "si"
   else:
      url = "confirmacion_asistencia"
      url2= "eliminar_asistencia"
      agendado = "Ya has agendado tu cita!"
      texto = "confirmar tu asistencia haz clic en el botón de abajo"
   context = {"url": f"{settings.YOUR_DOMAIN}/{url}/{cifrado}/", 
   "url2": f"{settings.YOUR_DOMAIN}/{url2}/{cifrado}/","username": username, "texto": texto, "agendado": agendado}
   template = get_template("correo.html")
   content = template.render(context)
   if confirmar == "registrar":
      email = EmailMultiAlternatives(
         "Verifica tu correo para empezar a usar Fisioamiga",
         "Fisioamiga",
         settings.EMAIL_HOST_USER,
         [mail]
      )
   else:
      email = EmailMultiAlternatives(
         "Confirmacion de asistencia",
         "Fisioamiga",
         settings.EMAIL_HOST_USER,
         [mail]
      )

   email.attach_alternative(content, "text/html")
   email.send()       

def confirmacion_correo(request, hash): 
   try:
      user = User.objects.filter(first_name=hash).first()
      user.is_active = True
      user.save()
      messages.success(request, "Ha confirmado su correo correctamente, ya posee el acceso para iniciar sesiòn en Fisioamiga")
      return redirect("index2")
   except:
      return HttpResponseNotFound("NotFound")

# cliente
@login_required(login_url='login')
def cliente_app(request):
   form = AgendaDiaForm(request.POST or None)
   form.fields['user'].queryset = User.objects.filter(id = request.user.id)
   if request.method == "POST":
         if form.is_valid():
            is_hola = Agenda.objects.filter(horario = request.POST["horario"])
            print(is_hola)
            if is_hola:
               messages.success(request, "El horario de dicha fecha no se encuentra disponible")
               return redirect('cliente')   
            form.save()
            messages.success(request, "Se ha agendado Correctamente")
            return redirect('cliente')
         else:
            print(request.POST)
            dt = datetime.strptime(request.POST["dia"], '%Y-%m-%d')
            today = datetime.today()
            if dt < today:
               messages.success(request, "No es posible agendar un dia ya pasado de la fecha")
               return redirect('cliente')
            messages.success(request, "Ha ocurrido un problema, vuelva a intentar")
            return redirect('cliente')
      
   else:
      context = {'form': form}
      return render(request, 'cliente_view/agendar.html', context)

@login_required(login_url='login')
def cliente_lista(request): 
   if request.method == "POST":
       pass
          
   else:
      object_list = CodigoConfirmacionHash.objects.filter(user=request.user)
      context = {'form': object_list}
      return render(request, 'cliente_view/lista_agenda.html', context)


def confirmacion_asistencia(request, hash): 
   try:
      user = CodigoConfirmacionHash.objects.filter(name=hash).first()
      user.status = "Aceptado"
      user.save()
      messages.success(request, "Ha confirmado su Asistencia")
      return redirect("cliente")
   except:
      return HttpResponseNotFound("NotFound")


def eliminar_asistencia(request, hash): 
   try:
      user = CodigoConfirmacionHash.objects.filter(name=hash).first()
      user.status = "Cancelado"
      user.save()
      messages.success(request, "Se ha cancelado la confirmacion")
      return redirect("cliente")
   except:
      return HttpResponseNotFound("NotFound")

