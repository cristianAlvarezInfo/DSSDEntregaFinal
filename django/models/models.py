from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
import json
from django.core import serializers
#pdf
from django.template.loader import get_template
from io import BytesIO
from django.http import HttpResponse
from xhtml2pdf import pisa

class SociedadAnonima(models.Model):
    class Meta:
        db_table = 'SociedadAnonima'
    nombre = models.CharField(max_length = 255, null = False)
    fecha_creacion = models.DateField(null=False)
    estatuto = models.FileField(null = False)
    domicilio_real = models.CharField(max_length = 255, null = False)
    domicilio_legal = models.CharField(max_length = 255, null = False)
    email_apoderado = models.EmailField()
    apoderado = models.OneToOneField('SocioSociedadAnonima', null = False, on_delete = models.CASCADE)
    paises_exporta = models.ManyToManyField('Pais')
    estados_exporta = models.ManyToManyField('Estado')
    estado_bonita = models.CharField(max_length = 50, null = True)  #Tarea en la que está
    numero_expediente = models.CharField(max_length=30,verbose_name='Numero de expediente',null=True)            #Numero unico, expediente bonita
    encrypted_id = models.CharField(max_length = 255, null = True)  #id para url
    url_qr = models.TextField(null = True)
    hash_estampilla = models.TextField(null = True)
    short_hash_estampilla = models.TextField(null = True)
    id_caso = models.IntegerField(null = True)                      #id caso bonita
    file_id_drive = models.TextField()                              #url del estatuto
    carpeta_fisica = models.TextField()

    def get_paises_json(self):
        prev = self.paises_exporta.all()
        paises = []
        for elem in prev:
            dict= elem.__dict__
            dict.pop('_state')
            paises.append(dict)
        return paises

    def get_estados_json(self):
        prev = self.estados_exporta.all()
        estados = []
        for elem in prev:
            dict= elem.__dict__
            dict.pop('_state')
            estados.append(dict)
        return estados

    def get_socios_json(self):
        prev = self.socios.all()
        socios = []
        for elem in prev:
            dict= elem.__dict__
            dict.pop('_state')
            socios.append(dict)
        return socios

    def diccionario(self):
        diccionario = {
            "id": self.id,
            "nombre": self.nombre,
            "fechaCreacion": self.fecha_creacion.__str__(),
            # "estatuto": self.estatuto,
            "domicilioReal": self.domicilio_real,
            "domicilioLegal": self.domicilio_legal,
            "emailApoderado": self.email_apoderado,
            "paisesExporta": self.get_paises_json(),
            "estadosExporta": self.get_estados_json(),
            "apoderado": {"nombre": self.apoderado.nombre,"apellido": self.apoderado.apellido,"porcentajeAportesRealizados": self.apoderado.porcentaje_aporte},
            "socios": self.get_socios_json(),
            "numero_expediente":self.numero_expediente,
            "encrypted_id": self.encrypted_id,
            "id_caso": self.id_caso,
            "file_id_drive": self.file_id_drive
            }
        return diccionario
    
    def render_to_pdf(self,template_src, context_dict={}):
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        destination = "/Users/matia/Desktop/" # ACA VA EL PATH DE DONDE SE VA A GUARDAR EL ARCHIVO PDF
        file = open(destination + context_dict['sociedad'].nombre + '.pdf', "w+b")
        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")),dest=file )
        #pdf = pisa.pisaDocument(StringIO(html.encode("UTF-8")),dest=result)
        if not pdf.err:
            return result.getvalue()
        return None

    def export_to_pdf (self):

        outfile = BytesIO()  # io.BytesIO() for python 3
        self.render_to_pdf('sociedad_anonima/sociedadAnonimaPDF.html',
            {
                'pagesize': 'A4',
                'sociedad': self,
            })
        response = HttpResponse(outfile.getvalue(), content_type='application/octet-stream')
        print('RESPONSE',response)
        response['Content-Disposition'] = 'attachment; filename= Sociedad Anonima expediente {}.pdf'.format(self.numero_expediente)
        return response


class SocioSociedadAnonima(models.Model):
    class Meta:
        db_table = 'SocioSociedadAnonima'
    nombre = models.CharField(max_length = 255, null = False)
    apellido = models.CharField(max_length = 255 , null = False)
    porcentaje_aporte = models.FloatField()
    sociedad = models.ForeignKey(SociedadAnonima, null = True, on_delete = models.CASCADE, related_name='socios') #Si es null, entonces es un apoderado


class Pais(models.Model):
    class Meta:
        db_table = 'Pais'
    codigo_gql = models.CharField(max_length = 255, null = False)

class Estado(models.Model):
    class Meta:
        db_table = 'Estado'
    nombre_gql = models.CharField(max_length = 255, null = False)
    pais_gql = models.CharField(max_length = 255, null = False)