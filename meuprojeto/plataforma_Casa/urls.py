from django.urls import path
from .views import  registrar_vaga, lista_vaga


urlpatterns = [
    path('registrar-vaga/', registrar_vaga, name='registrar_vaga'),
    path('listar-vagas/', lista_vaga, name='lista_vagas'),
]