from django.shortcuts import render
from .service import VagasService

def registrar_vaga(request):
    vagas_service = VagasService()
    contexto = vagas_service.vagas_service(request)
    return render(request, 'registrar_vaga.html', contexto)

def lista_vaga(request):
    vagas_service = VagasService()
    vagas = vagas_service.listar_vagas_ativas()
    contexto = {
        'vagas': vagas
    }
    return render(request, 'lista_vagas.html', contexto)