import os

from datetime import date
from models.models import *

from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db.models import Count


class Repository(object):
    def find_user_by_email(self, email):
        users_filtered = User.objects.filter(username = email)
        return users_filtered[0] if len(users_filtered) > 0 else None

    def add_user(self, email, password):
        if not self.find_user_by_email(email):
            user = User.objects.create_user(username = email, password = password)
            return True
        return False

    def create_apoderado(self, nombre, apellido, porcentaje):
        apoderado =  SocioSociedadAnonima(nombre = nombre,apellido = apellido,porcentaje_aporte = porcentaje)
        apoderado.save()
        return apoderado

    def findPiasByCodigGQL(self,codigo_gql):
        paises_filtered = Pais.objects.filter(codigo_gql=codigo_gql)
        return paises_filtered[0] if len(paises_filtered) > 0 else None    

    def create_pais(self, codigo_gql):
        pais = self.findPiasByCodigGQL(codigo_gql)
        if pais:
           return pais
        pais = Pais(codigo_gql = codigo_gql)
        pais.save()
        return pais
    
    def findEstadoByNameGQL(self,nombre_gql):
        estados_filtered = Estado.objects.filter(nombre_gql=nombre_gql)
        return estados_filtered[0] if len(estados_filtered) > 0 else None    

    def create_estado(self, nombre_gql, code_pais_gql):
        estado = self.findEstadoByNameGQL(nombre_gql)
        if estado:
            return estado
        estado = Estado(nombre_gql = nombre_gql, pais_gql = code_pais_gql)
        estado.save()
        return estado

    def add_sociedad_anonima(self, data):
        apoderado = self.create_apoderado(nombre = data['nombre_apoderado'], 
                    apellido = data['apellido_apoderado'], porcentaje = data['porcentajeApoderado'])
        
        sociedad_anonima = SociedadAnonima(nombre = data['nombre'],fecha_creacion = date.today() ,estatuto = data['estatuto'],
                        domicilio_real=data['domicilio_real'],domicilio_legal=data['domicilio_legal'],email_apoderado=data['email_apoderado'],
                        apoderado = apoderado)
        sociedad_anonima.save()
        sociedad_anonima.encrypted_id = '0' # TODO encriptar el sociedad_anonima.id y guardarlo
        sociedad_anonima.save()

        if(len(data['paises'])== 0):
            # Si no vienen paises, por defecto definimos a argentina
            pais = self.create_pais("AR")
            sociedad_anonima.paises_exporta.add(pais)
        else:
            for codigo_pais in data['paises']:
                pais = self.create_pais(codigo_pais)
                sociedad_anonima.paises_exporta.add(pais)
        
        # Agregamos los estados a los que se exporta en la bd
        for estado in data['estados']:
            nombre_estado_gql = estado.split(':')[0]
            code_pais_gql = estado.split(':')[1]
            estado = self.create_estado(nombre_estado_gql,code_pais_gql)
            sociedad_anonima.estados_exporta.add(estado)
            
        for socio in data['socios']:
            socio = self.create_apoderado(nombre = socio['nombre'], apellido = socio['apellido'], porcentaje = socio['porcentaje'])
            socio.sociedad = sociedad_anonima
            socio.save()

        return sociedad_anonima

    def sociedades_anonimas(self):
        return SociedadAnonima.objects.all()

    def altas_by_date(self):
        return(SociedadAnonima.objects
            .values('fecha_creacion')
            .annotate(dcount=Count('fecha_creacion'))
            .order_by())

    def sociedad_anonima(self, id_sociedad):
        return SociedadAnonima.objects.get(id=id_sociedad)

    def update_country_states(self,sociedad,countries, states):
        # Eliminamos las filas de paises y estados ya que cambiaron
        sociedad.paises_exporta.clear()
        sociedad.estados_exporta.clear()

        if len(countries) == 0:
            # Si no vienen paises, por defecto definimos a argentina
            pais = self.create_pais("AR")
            sociedad.paises_exporta.add(pais)

        # Reactualizamos paises
        for codigo_pais in countries:
            pais = self.create_pais(codigo_pais)
            sociedad.paises_exporta.add(pais)
        
        # Reactualizamos estados
        for estado in states:
            nombre_estado_gql = estado.split(':')[0]
            code_pais_gql = estado.split(':')[1]
            estado = self.create_estado(nombre_estado_gql,code_pais_gql)
            sociedad.estados_exporta.add(estado)

    def update_sociedad(self, sociedad_anonima, datos_sociedad, file, ):
        if file is not None:
            sociedad_anonima.estatuto = file.name 
            # Eliminar el viejo y poner el nuevo
            BASE_PATH_FILE = str(os.path.abspath(os.getcwd()))
            default_storage.save(f'{BASE_PATH_FILE}/media/{file.name}', file) # Save new file in local


        countries = datos_sociedad.getlist('countries')
        states = datos_sociedad.getlist('states')
        self.update_country_states(sociedad_anonima, countries, states)

        sociedad_anonima.nombre = datos_sociedad.get('nombre')
        sociedad_anonima.apoderado.porcentaje_aporte = datos_sociedad.get('porcentajeApoderado')
        sociedad_anonima.apoderado.nombre = datos_sociedad.get('nombre_apoderado')
        sociedad_anonima.apoderado.apellido = datos_sociedad.get('apellido_apoderado')
        sociedad_anonima.domicilio_real = datos_sociedad.get('domicilio_real')
        sociedad_anonima.domicilio_legal = datos_sociedad.get('domicilio_legal')
        sociedad_anonima.apoderado.save()
        sociedad_anonima.save()
        socios=sociedad_anonima.socios.all()
        for i in range(len(socios)):
            socio=socios[i]
            socio.nombre=datos_sociedad.getlist('nombre_socio')[i]
            socio.apellido=datos_sociedad.getlist('apellido_socio')[i]
            socio.porcentaje_aporte=datos_sociedad.getlist('porcentajeSocio')[i]
            socio.save()


    def find_sociedad_by_num_expediente(self, num_expediente):
        print('num expediente',num_expediente)
        sociedad = SociedadAnonima.objects.filter(numero_expediente = num_expediente)
        print(sociedad)
        return sociedad[0] if len(sociedad) > 0 else None    

    def find_sociedad_by_short_hash_estampilla(self, short_hash_estampilla):
        print(list(SociedadAnonima.objects.all())[-1].__dict__)
        sociedad = SociedadAnonima.objects.filter(short_hash_estampilla = short_hash_estampilla)
        return sociedad[0] if len(sociedad) > 0 else None   

    def socios(self, id_sociedad):
        return SocioSociedadAnonima.objects.filter(sociedad = id_sociedad)

    def sociedades_anonimas_by_cases(self,active_cases):
        return SociedadAnonima.objects.filter(id_caso__in = active_cases)

    def set_num_exp(self, num_exp, case_id):
        sociedad = SociedadAnonima.objects.filter(id_caso= case_id).first()
        sociedad.numero_expediente = num_exp
        sociedad.save()
