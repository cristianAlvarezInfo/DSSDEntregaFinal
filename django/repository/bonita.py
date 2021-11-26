import requests

class Bonita(object):
    def __init__(self):
        self._id_user = None
        self._cookies = None
        self._token = None
        self._processID = None
        self._URL = 'http://localhost:8090'

    def cookies(self):
        return self._cookies
    
    def token(self):
        return self._token

    def processID(self):
        return self._processID

    def get_processID_after_login(self, cookies, token):
        headers = {'Cookie': cookies, 'X-Bonita-API-Token': token}
        URL = f'{self._URL}/bonita/API/bpm/process?p=0&c=10'
        response = requests.request('GET', URL, headers = headers)
        if response.status_code == 200:
            data = response.json()
            process_workflow = list(filter(lambda x: x['name'] == "Workflow",data))[0]
            self._processID = process_workflow['id']
            return self._processID
        return -1

    def _parse_cookies(self, response):
        cookies = ''
        for key in response.cookies.keys():
            valor = key + '=' + response.cookies[key] + ';'
            cookies += valor
        return cookies

    def create_user(self):
        pass
    
    def login_user(self, username, password):
        '''
            Log a user in bonita
        '''
        body = { 'username': username, 'password': password }
        headers = { 'Content-type': 'application/x-www-form-urlencoded','Accept': 'application/json' }
        response = requests.request("POST",f'{self._URL}/bonita/loginservice',params = body, headers = headers)
        self._cookies = self._parse_cookies(response)
        self._token = response.cookies.get('X-Bonita-API-Token')
        process_id = self.get_processID_after_login(self._cookies, self._token)
        return [self._cookies, self._token, process_id, response]   

    def get_user_id(self, username, token = None, cookies = None):
        '''
            Returns user_id from bonita
        '''
        headers = {
            'Content-Type': 'application/json',
            'X-Bonita-API-Token': self._token if(token is None) else token,
            'Cookie': self._cookies if(cookies is None) else cookies
        }
        URL = f'{self._URL}/bonita/API/identity/user?f=userName={username}'
        response = requests.request('GET', URL, headers = headers)
        if response.status_code == 200:
            json = response.json()
            try:
                self._id_user = json[0]['id']
                return self._id_user
            except:
                # El user no existe en bonita
                return -1
        return -1

    def has_user_role(self, user_id, role_name, token = None, cookies = None):
        '''
            Returns if user has named rol
        '''
        headers = {
            'Content-Type': 'application/json',
            'X-Bonita-API-Token': self._token if(token is None) else token,
            'Cookie': self._cookies if(cookies is None) else cookies
        }
        URL = f'{self._URL}/bonita/API/identity/membership?p=0&c=10&f=user_id={user_id}&d=role_id&d=user_id'
        response = requests.request('GET', URL, headers = headers)
        if response.status_code == 200:
            try:
                user_rol = response.json()[0]['role_id']['name']
                return user_rol == role_name
            except:
                return False
        return False
        
    def send_sociedad_anonima(self, id_sociedad_anonima):
        '''
            Save a case in bonita
        '''
        proceso = {'s': 'Workflow'}
        header = {'Cookie': self._cookies,'Content-Type':'application/json'}
        response = requests.request("GET", f'{self._URL}/bonita/API/bpm/process', params= proceso, headers= header)
        id_proceso = response.json()[0]['id']

        # Creamos el case
        header = {'X-Bonita-API-Token': str(self._token),"cookie": self._cookies}
        body1='{"processDefinitionId":'+ str(id_proceso) + '}'
        response = requests.request("POST",f'{self._URL}/bonita/API/bpm/case', headers=header,data=body1) 
        id_caso=response.json()["id"]     
           
        # Seteamos el valor de la petición para el alta
        body2 = '{"type":"java.lang.String","value": ' + str(id_sociedad_anonima) + '}'
        url=f'{self._URL}/bonita/API/bpm/caseVariable/{id_caso}/id_pedido'
        response = requests.request("PUT",url, headers=header,data=body2)
        return id_caso 

    def get_active_cases(self, cookies, token, whois = None):
        headers = {'Cookie': cookies, 'X-Bonita-API-Token': token}
        URL = f'{self._URL}/API/bpm/case?p=0&c=10&f=name=Workflow'
        response = requests.request('GET', URL, headers = headers)
        if response.status_code == 200:
            data = response.json()
            active_cases = [case['id'] for case in data]
            return [active_cases, response]
        return [[], response]

    def get_active_tasks_by_name(self, cookies, token, task_name = None):
        '''
            Return the active cases for a task
        '''
        headers = {'Cookie': cookies, 'X-Bonita-API-Token': token}
        # TODO interpolar process id obteniendolo del workflow
        URL = f'{self._URL}/bonita/API/bpm/task?c=10&p=0&f=processId={self.get_processID_after_login(cookies,token)}&f=name={task_name}&o=state'
        # Determinar la validez del trámite
        response = requests.request('GET', URL, headers = headers)
        if response.status_code == 200:
            data = response.json()
            active_cases = [{'case_id': case['caseId'], 'task_id': case['id'], 'assigned_id': case['assigned_id']} for case in data]
            return [active_cases, response]
        return [[], response]   

    def update_bonita_variable(self, cookies, token, case_id, variable_name, value, type = 'java.lang.String'):
        '''
            El type solo admite  java.lang.String, java.lang.Integer, java.lang.Double, 
            java.lang.Long, java.lang.Boolean, java.util.Date
        '''
        URL = f'{self._URL}/bonita/API/bpm/caseVariable/{str(case_id)}/{variable_name}'
        headers = {'Cookie': cookies, 'X-Bonita-API-Token': token}
        body = '{"type": "' + str(type) + '","value": "' + str(value) + '"}'
        response = requests.request('PUT', URL, headers = headers, data = body)
        return response
    
    
    def change_task_state(self, cookies, token, task_id, state, user_id):
        '''
            Tipos de estados de tareas: INITIALIZING, STARTED, SUSPENDED, 
            CANCELLED, ABORTED, COMPLETING, COMPLETED, ERROR, ABORTING
        '''
        URL = f'{self._URL}/bonita/API/bpm/userTask/{str(task_id)}'
        headers = {'Cookie': cookies, 'X-Bonita-API-Token': token}
        body = '{"assigned_id": "' + str(user_id) + '","state": "' + str(state) + '"}'
        response = requests.request('PUT', URL, headers = headers, data = body)
        return response

    def assign_task_to_user(self, cookies, token, task_id, user_id):
        ''' 
        PUT /API/bpm/userTask/:userTaskId
        {
          "assigned_id" : "id of new user",
          "state":"skipped"
        }
        '''
        URL = f'{self._URL}/bonita/API/bpm/userTask/{task_id}'
        headers = {'Cookie': cookies, 'X-Bonita-API-Token': token}
        body = '{"assigned_id": "' + str(user_id) + '"}'
        response = requests.request('PUT', URL, headers = headers, data = body)
        return response
