import os
import json
from django.http import *
from django.views import View

from datetime import datetime

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
    print(query)
    headers = {'content-type': 'application/json'}
    response = requests.post('https://countries.trevorblades.com/', json=query, headers=headers)
    return response.json()['data']['countries']


def get_states(selected_countries):
    def get_country_query(country_code):
        return '{ country(code: "' + country_code + '") { states { name } } }'
    
    states = {}
    states_name = []
    for country_code in selected_countries:
        query = {
            "query": get_country_query(country_code)
        }
        print(query)
        headers = {'content-type': 'application/json'}
        response = requests.post('https://countries.trevorblades.com/', json=query, headers=headers)
        states_json = response.json()['data']['country']['states']
        states[country_code] = states_json
    return states

class RegistroSAView(View):
    def get(self,request):
        return render(request,'sociedad_anonima/register.html', context={'countries': get_countries()})

    def post(self,request):
        #bonita.login_user(username = 'anonima', password = 'bpm') #DESCOMENTAR
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
        # bonita.login_user('apoderado', 'bpm')
        sociedad_anonima = repository.add_sociedad_anonima(data)
        # id_caso = bonita.send_sociedad_anonima(sociedad_anonima)
        # sociedad_anonima.id_caso = id_caso
        sociedad_anonima.id_caso = 1
        sociedad_anonima.save()

        # Cambia de estado a completado
        # [active_cases, response] = bonita.get_active_tasks_by_name(bonita.cookies(), bonita.token(), 'Llenado de formulario de Alta SA')
        # active_case = list(filter(lambda x: x['case_id'] == id_caso,active_cases))[0]
        # user_id = bonita.get_user_id('apoderado', cookies = bonita.cookies(), token = bonita.token())
        # bonita.change_task_state(bonita.cookies(), bonita.token(), active_case['task_id'], 'completed', user_id)

        return redirect('/')

class SociedadAnonimaDetail(View):
    def get(self, request, hash_id):
        # TODO desencriptar el id que llega, ahora viene plano
        sociedad_anonima = repository.find_sociedad_by_short_hash_estampilla(hash_id)
        if not sociedad_anonima:
            context = { 'found': False, 'sociedad_anonima': sociedad_anonima }
        else:
            context = { 'found': True, 'sociedad_anonima': sociedad_anonima }
        return render(request, 'sociedad_anonima/sociedadAnonimaDetail.html', context)


class SociedadAnonimaCorreccionMesaEntrada(View):
    def __complete_task_bonita(self, expired_token, id_caso):
        id_caso = str(id_caso)
        [cookies, token, process_id, response] = bonita.login_user('apoderado','bpm')
        bonita.update_bonita_variable(cookies, token, id_caso, 'vencioPlazo', expired_token, 'java.lang.Boolean')
        [active_cases, response] = bonita.get_active_tasks_by_name(bonita.cookies(), bonita.token(), 'Corrección de formulario')
        print('ID CASO ',id_caso)
        print('Active cases ',active_cases)
        try:
            active_case = list(filter(lambda x: x['case_id'] == id_caso,active_cases))[0]
        except:
            return 
        user_id = bonita.get_user_id('apoderado', cookies = cookies, token = token)
        bonita.change_task_state(cookies, token, active_case['task_id'], 'completed', user_id)

    def get(self, request, id_sociedad, fecha_limite, id_caso):
        fecha_limite_param = fecha_limite
        fecha_limite = self.__format_date(fecha_limite)
        fecha_actual = datetime.now()
        expired_token = False
        if fecha_limite < fecha_actual:
            # El token se vencio
            expired_token = True
            self.__complete_task_bonita(True, id_caso)
        try:
            sociedad_anonima = repository.sociedad_anonima(id_sociedad)
            selected_countries_codes = list(map(lambda x: x.codigo_gql, sociedad_anonima.paises_exporta.all()))
            selected_states_names = list(map(lambda x: x.nombre_gql, sociedad_anonima.estados_exporta.all()))
            states = get_states(selected_countries_codes)
            action_url = f'/SA/correciones_mesa_entrada/{id_sociedad}/{fecha_limite_param}/{id_caso}'
            context = {
                'existe_sociedad': True, 
                'sociedad_anonima': sociedad_anonima, 
                'expired': expired_token, 
                "action_url": action_url, 
                'countries': get_countries(), 
                'states': states,
                'selected_countries_code': selected_countries_codes,
                'selected_states_name': selected_states_names,
            }    
        except:
            context = {'existe_socidad': False, 'expired': expired_token, 'countries': []}
        return render(request, 'sociedad_anonima/correcciones.html', context)
    
    def post(self, request, id_sociedad, fecha_limite, id_caso):
        fecha_limite = self.__format_date(fecha_limite)
        fecha_actual = datetime.now()
        if fecha_limite >= fecha_actual:
            # El token no expiro
            #self.__complete_task_bonita(False, id_caso) #DESCOMENTAR
            # Actualizamos la DB
            sociedad_anonima = repository.sociedad_anonima(id_sociedad)
            repository.update_sociedad(sociedad_anonima, request.POST)
            return redirect('/')

        # Por aca expiro
        context = { 'expired': True }
        self.__complete_task_bonita(True, id_caso)
        return render(request, 'sociedad_anonima/correcciones.html', context)


    def __format_date(self, fecha_limite):
        fecha_limite=fecha_limite.replace("-","/")
        fecha_limite = datetime.strptime(fecha_limite, "%d/%m/%Y")
        return fecha_limite   


class SociedadAnonimaCorreccionAreaLegales(View):
    def __complete_task_bonita(self, id_caso):
        id_caso = str(id_caso)
        [cookies, token, process_id, response] = bonita.login_user('apoderado','bpm')
        [active_cases, response] = bonita.get_active_tasks_by_name(bonita.cookies(), bonita.token(), 'Corregir estatuto')
        try:
            active_case = list(filter(lambda x: x['case_id'] == id_caso,active_cases))[0]
        except:
            return 
        user_id = bonita.get_user_id('apoderado', cookies = cookies, token = token)
        bonita.change_task_state(cookies, token, active_case['task_id'], 'completed', user_id)

    def get(self, request, id_sociedad, id_caso):
        try:
            sociedad_anonima = repository.sociedad_anonima(id_sociedad)
            action_url = f'/SA/correciones_area_legales/{id_sociedad}/{id_caso}'
            context = {'existe_sociedad': True, 'sociedad_anonima': sociedad_anonima, 'expired': False, "action_url": action_url}    
        except:
            context = {'existe_socidad': False, 'expired': False}
        return render(request, 'sociedad_anonima/correcciones.html', context)
    
    def post(self, request, id_sociedad, id_caso):
        sociedad_anonima = repository.sociedad_anonima(id_sociedad)
        repository.update_sociedad(sociedad_anonima, request.POST)
        self.__complete_task_bonita(id_caso)
        return redirect('/')
