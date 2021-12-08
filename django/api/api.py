import os
import json
from django.http import JsonResponse
from repository.repository import Repository
from repository.bonita import Bonita
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from repository.utils import create_pdf_with_content

repository = Repository()
bonita = Bonita()

# POST /api/sociedades_anonimas
# No se usa porque devuelve todos las active cases del proceso
@method_decorator(csrf_exempt)
def sociedades_anonimas(request):
    response = JsonResponse({})
    if request.method == 'POST':
        cookies = request.POST.get('cookies')
        token = request.POST.get('token')
        [active_cases, response] = bonita.get_active_cases(cookies, token)
        sociedades_anonimas = repository.sociedades_anonimas_by_cases(active_cases)
        sociedades_anonimas = list(map(lambda sociedad: sociedad.diccionario(), sociedades_anonimas))
        # [{},{}]
    response = JsonResponse({'state': response.status_code, 'ok': response.status_code == 200, 'data': json.loads(json.dumps(sociedades_anonimas))})
    response["Access-Control-Allow-Origin"] = "*"
    return response


# GET /api/sociedad_anonima/:id
@method_decorator(csrf_exempt)
def sociedad_anonima(request, id):
    print(request.headers)
    sociedad = repository.sociedad_anonima(id)
    serialized_sociedad = {
        'id': sociedad.id,
        'nombre': sociedad.nombre,
        'email_apoderado': sociedad.email_apoderado
    }
    response = JsonResponse({'state': 200, 'ok': True, 'data': json.loads(json.dumps(serialized_sociedad))})
    response["Access-Control-Allow-Origin"] = "*"
    return response

@method_decorator(csrf_exempt)
def login_bonita(request):
    response = JsonResponse({})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        [cookies, token, process_id, response] = bonita.login_user(username,password)
        if response.status_code == 204:
            data = {
                'Cookie': cookies,
                'Token': token,
                'processID': process_id,
                'ok': True
            }
        else:
            data = {'info': 'Invalid User','ok': False}
        response = JsonResponse(data)
    
    response["Access-Control-Allow-Origin"] = "*"  # OJO CON EL PUERTOO!!!!!
    response["Access-Control-Allow-Methods"] = "GET, POST"
    return response

@method_decorator(csrf_exempt)
def get_user_id(request):
    response = JsonResponse({})
    if request.method == 'POST':
        username = request.POST.get('username')
        token = request.POST.get('token')
        cookies = request.POST.get('cookies')
        user_id = bonita.get_user_id(username, token = token, cookies = cookies)
        if user_id == -1:
            data = { 'user_id': -1 , 'ok': False }
        else:
            data = { 'user_id': user_id, 'ok': True }
        response = JsonResponse(data)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST"
    return response


# POST /api/mesa_de_entrada/validacion_sociedades_anonimas
@method_decorator(csrf_exempt)
def get_sociedades_anonimas_by_task_name(request):
    response = JsonResponse({})
    if request.method == 'POST':
        cookies = request.POST.get('cookies')
        token = request.POST.get('token')
        task_name = request.POST.get('task_name')
        [active_cases, response] = bonita.get_active_tasks_by_name(cookies, token, task_name)
        list_id_cases = list(map(lambda x: x['case_id'], active_cases))
        sociedades_anonimas = repository.sociedades_anonimas_by_cases(list_id_cases)
        # Asociamos a cada sociedad con su task_id
        sociedades_with_taskid = []
        for case in active_cases:
            # Filtrar la sociedad que tenga este case
            filtered_sociedad_anonima = list(filter(lambda x: x.id_caso == int(case['case_id']), sociedades_anonimas))[0]
            sociedades_with_taskid.append({
                'case_id': case['case_id'],
                'task_id': case['task_id'],
                'assigned_id': case['assigned_id'],
                'data': filtered_sociedad_anonima.diccionario()
            })
    response = JsonResponse({'state': response.status_code, 'ok': response.status_code == 200, 'data': json.loads(json.dumps(sociedades_with_taskid))})
    response["Access-Control-Allow-Origin"] = "*"
    return response

# POST /api/update_variable/
@method_decorator(csrf_exempt)
def update_case_variable(request):
    response = JsonResponse({})
    if request.method == 'POST':
        variable_name = request.POST.get('variable_name')
        value_variable = request.POST.get('value_variable')
        type_variable = request.POST.get('type_variable')
        case_id = request.POST.get('case_id')
        cookies = request.POST.get('cookies')
        token = request.POST.get('token')
        # [cookies, token, process_id, response] = bonita.login_user('walter.bates', 'bpm')
        response = bonita.update_bonita_variable(cookies, token, case_id, variable_name, value_variable, type_variable)
    response = JsonResponse({'state': response.status_code, 'ok': response.status_code == 200})
    response["Access-Control-Allow-Origin"] = "*"
    return response

# POST /api/change_task_state
@method_decorator(csrf_exempt)
def change_task_state(request):
    response = JsonResponse({})
    if request.method == 'POST':
        cookies = request.POST.get('cookies')
        token = request.POST.get('token')
        user_id = request.POST.get('user_id')
        state = request.POST.get('new_state')
        task_id = request.POST.get('task_id')
        # [cookies, token, process_id, response] = bonita.login_user('william.jobs', 'bpm')
        # user_id = bonita.get_user_id('william.jobs', cookies = cookies, token = token)
        response = bonita.change_task_state(cookies, token, task_id, state, user_id)
    response = JsonResponse({'state': response.status_code, 'ok': response.status_code == 200})
    response["Access-Control-Allow-Origin"] = "*"
    return response

@method_decorator(csrf_exempt)
def assign_task_to_user(request):
    response = JsonResponse({})
    if request.method == 'POST':
        cookies = request.POST.get('cookies')
        token = request.POST.get('token')
        user_id = request.POST.get('user_id')
        task_id = request.POST.get('task_id')
        response = bonita.assign_task_to_user(cookies, token, task_id, user_id)
    response = JsonResponse({'state': response.status_code, 'ok': response.status_code == 200})
    response["Access-Control-Allow-Origin"] = "*"
    return response

@method_decorator(csrf_exempt)
def assign_num_exp(request):
    response = JsonResponse({})
    if request.method == 'POST':
        #cookies = request.POST.get('cookies')
        #token = request.POST.get('token')
        result = json.loads(request.body)
        num_exp = result['num_exp']
        case_id = result['case_id']
        repository.set_num_exp(num_exp,case_id)
    response = JsonResponse({'state': response.status_code, 'ok': response.status_code == 200})
    response["Access-Control-Allow-Origin"] = "*"
    return response

@method_decorator(csrf_exempt)
def login_role_bonita(request):
    response = JsonResponse({})
    if request.method == 'POST':
        [cookies, token, process_id, response] = bonita.login_user('walter.bates','bpm')
        print('Cookies ',cookies, ' ',token, ' ',process_id)
        username = request.POST.get('username')
        user_id = bonita.get_user_id(username, cookies = cookies, token = token)
        if user_id == -1:
            # The user doesnt exists
            response = JsonResponse({'state': 403, 'ok': False})
            response["Access-Control-Allow-Origin"] = "*"
            return response
        role_name = request.POST.get('role_name')
        has_rol = bonita.has_user_role(user_id, role_name, cookies = cookies, token = token)
        print(f'TIene rol ',has_rol)
        if not has_rol:
            response = JsonResponse({'state': 403, 'ok': False})
            response["Access-Control-Allow-Origin"] = "*"
            return response
        password = request.POST.get('password')
        [cookies, token, process_id, response] = bonita.login_user(username, password)
        data = {
            'Cookie': cookies,
            'Token': token,
            'processID': process_id,
            'ok': True,
            'state': 200
        }
        response = JsonResponse(data)
    response["Access-Control-Allow-Origin"] = "*"
    return response

@method_decorator(csrf_exempt)
def update_estampilla_qr(request):
    response = JsonResponse({})
    if request.method == 'POST':
        result = json.loads(request.body)
        numero_expediente = result['numero_expediente']
        hash_estampilla = result['estampilla']
        short_hash_estampilla = result['short_hash'] # Representa una parte identificatoria de la estampila
        url_qr = result['url_qr']
        sociedad = repository.find_sociedad_by_num_expediente(numero_expediente)
        if sociedad:
            sociedad.url_qr = url_qr
            sociedad.hash_estampilla = hash_estampilla
            sociedad.short_hash_estampilla = short_hash_estampilla
            sociedad.save()
            response = JsonResponse({'state': 200, 'ok': True})
        else:
            response = JsonResponse({'state': 500, 'ok': False})
    response["Access-Control-Allow-Origin"] = "*"
    return response

@method_decorator(csrf_exempt)
def ping(request):
    response = JsonResponse({'data': 'Pong!'})
    response["Access-Control-Allow-Origin"] = "*"
    return response

@method_decorator(csrf_exempt)
def export_to_pdf(request):
    response = JsonResponse({})
    if request.method == 'POST':
        body = json.loads(request.body)
        print(body)
        filename = body['filename']
        content = body['content']
        id_sociedad = body['idSociedad']
        create_pdf_with_content(content,filename)

        BASE_PATH_FILE = str(os.path.abspath(os.getcwd()))
        sociedad = repository.sociedad_anonima(id_sociedad)
        sociedad.carpeta_fisica = f'{BASE_PATH_FILE}/media/{filename}'
        sociedad.save()

 
    response = JsonResponse({'state': response.status_code, 'ok': response.status_code == 200})
    response["Access-Control-Allow-Origin"] = "*"
    return response



