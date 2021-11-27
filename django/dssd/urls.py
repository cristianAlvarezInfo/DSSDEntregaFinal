"""dssd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from .views import *
from django.contrib import admin
from dssd import views
from django.urls import path
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from dssd import views as v
from api import api
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name = 'home'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', logout_view, name = 'logout'),
    path('registro_sa/',RegistroSAView.as_view()),
    path('SA/<str:hash_id>', SociedadAnonimaDetail.as_view()),
    path('SA/correciones_mesa_entrada/<int:id_sociedad>/<str:fecha_limite>/<int:id_caso>', SociedadAnonimaCorreccionMesaEntrada.as_view()),
    path('SA/correciones_area_legales/<int:id_sociedad>/<int:id_caso>', SociedadAnonimaCorreccionAreaLegales.as_view()),
    path('api/ping/', api.ping , name='login_bonita'),
    path('api/login_bonita/', api.login_bonita , name='login_bonita'),
    path('api/login_role_bonita/', api.login_role_bonita , name='login_role_bonita'),
    path('api/bonita_user_id/', api.get_user_id , name='get_user_id'),
    path('api/update_variable/', api.update_case_variable , name='update_case_variable'),
    path('api/update_estampilla_qr/', api.update_estampilla_qr , name='update_estampilla_qr'),
    path('api/change_task_state/', api.change_task_state , name='change_task_state'),
    path('api/sociedades_anonimas/', api.sociedades_anonimas , name='sociedades_anonimas'),
    path('api/sociedad_anonima/<int:id>', api.sociedad_anonima , name='sociedad_anonima'),
    path('api/get_sociedades_anonimas_by_task_name/', api.get_sociedades_anonimas_by_task_name , name='get_sociedades_anonimas_by_task_name'),
    path('api/assign_task_to_user/', api.assign_task_to_user , name='assign_task_to_user'),
    path('api/assign_numero_expediente/', api.assign_num_exp , name='assign_num_exp'),
]
