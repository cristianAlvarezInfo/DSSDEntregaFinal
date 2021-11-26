import os
import json
from django.http import *
from django.views import View

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import requests

from forms.forms import *
from django.views.decorators.csrf import csrf_exempt

from repository.bonita import Bonita
from repository.repository import Repository
from repository.utils import upload_file_drive, list_files_uploaded

# from rest_framework.views import APIView
# from rest_framework import permissions
# from rest_framework.response import Response

bonita = Bonita()
repository = Repository()

def home(request):
    return render(request, 'layout.html')

def logout_view(request):
    logout(request)
    return redirect('/')

class VistaRegistro(View):   
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'user/register.html')

    @csrf_exempt
    def post(self, request):
        context = {"error": "El formato de los datos ingresados son incorrectos"}
        formulario = FormularioRegistro(request.POST)
        if formulario.is_valid():
            saved = repository.add_user(email = request.POST.get("email"), password = request.POST.get("password"))
            if saved:
                return redirect('/')
            context['error'] = "El usuario ya existe"
        return render(request, 'user/register.html', context)

class LoginView(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('/alta_formulario')
        return render(request, 'user/login.html')
    
    @csrf_exempt
    def post(self,request):
        from django.contrib.auth.models import User
        [cookies, token, process_id, response] = bonita.login_user(request.POST.get("email"), request.POST.get("password"))
        username = request.POST.get("email")
        if response.status_code == 204:   
            user = authenticate(username = username, password = request.POST.get("password"))     
            if user is None:
                user = User.objects.create_user(username = username, password = request.POST.get("password"))
            user_id = bonita.get_user_id(username)
            login(request, user)
            return redirect('/')
        return render(request, 'user/login.html', {"error": "Los datos ingresados son incorrectos"})


def get_countries():
    query = {
        "query": '{ countries { code, name, states { name } } }'
    }
    
    headers = {'content-type': 'application/json'}
    response = requests.post('https://countries.trevorblades.com/', json=query, headers=headers)
    return response.json()['data']['countries']

class RegistroSAView(View):
    def get(self,request):
        list_files_uploaded()
        return render(request,'sociedad_anonima/register.html', context={'countries': get_countries()})

    def post(self,request):
        bonita.login_user(username = 'anonima', password = 'bpm')
        data = {
            'nombre': request.POST.get('nombre'),
            'porcentajeApoderado': float(request.POST.get('porcentajeApoderado')),
            'estatuto': request.POST.get('estatuo'),
            'domicilio_legal': request.POST.get('domicilio_legal'),
            'domicilio_real': request.POST.get('domicilio_real'),
            'nombre_apoderado': request.POST.get('nombre_apoderado'),
            'apellido_apoderado': request.POST.get('apellido_apoderado'),
            'email_apoderado': request.POST.get('email_apoderado'),
        }
        
        # Save file first in local and then in drive
        file = request.FILES['estatuo']
        BASE_PATH_FILE = str(os.path.abspath(os.getcwd()))
        default_storage.save(f'{BASE_PATH_FILE}/media/{file.name}', file) # Save file in local
        file_id_drive = upload_file_drive(file.name) 
        print("id archivo: ", file_id_drive)

        nombre_socios = request.POST.getlist('nombre_socio')
        apellido_socios = request.POST.getlist('apellido_socio')
        porcentaje_socios = request.POST.getlist('porcentajeSocio')
        
        socios = []
        for i in range(len(nombre_socios)):
            socios.append({
                'nombre': nombre_socios[i] , 
                'apellido': apellido_socios[i], 
                'porcentaje': float(porcentaje_socios[i])
            })
        data['socios'] = socios
        data['paises'] = request.POST.getlist('countries')
        data['estados'] = request.POST.getlist('states')
        data['file_id_drive'] = file_id_drive
        bonita.login_user('anonimo', 'bpm')
        sociedad_anonima = repository.add_sociedad_anonima(data)
        id_caso = bonita.send_sociedad_anonima(sociedad_anonima)
        sociedad_anonima.id_caso = id_caso
        sociedad_anonima.save()
        return redirect('/')

class SociedadAnonimaDetail(View):
    def get(self, request, hash_id):
        # TODO desencriptar el id que llega, ahora viene plano
        try:
            sociedad_anonima = repository.sociedad_anonima(id)
            socios = repository.socios(id)
            self._generate_qr(sociedad_anonima)
            context = { 'found': True, 'sociedad_anonima': sociedad_anonima, 'socios': socios }
        except:
            context = { 'found': False, 'sociedad_anonima': None } 
        return render(request, 'sociedad_anonima/sociedadAnonimaDetail.html', context)


