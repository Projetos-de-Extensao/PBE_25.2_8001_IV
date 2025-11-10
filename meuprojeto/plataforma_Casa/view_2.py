from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .permission import (
            is_adm, 
            is_admin_user, 
            is_aluno_access, 
            is_monitor_access, 
            is_funcionairo_access
            )
from .service import VagaService, UsuarioService

from .models import Vaga, Inscricao, Curso, Usuario, TipoUsuario


# Criado o VagaService para encapsular a lógica de negócio da view detalhe_vaga
@login_required
@user_passes_test(is_funcionairo_access)
def detalhe_vaga(request, vaga_id):
    """
    View refatorada: delega toda lógica para VagaService e apenas renderiza o contexto.
    """
    try:
        service = VagaService(vaga_id, request.user)
        context = service.get_context()
    except PermissionDenied:
        messages.error(request, '❌ Você não tem permissão para ver esta vaga')
        return redirect('listar_vagas')
    except Exception as e:
        messages.error(request, f'❌ Erro ao carregar vaga: {str(e)}')
        return redirect('listar_vagas')

    return render(request, 'vagas/detalhe.html', context)


@login_required
@user_passes_test(is_aluno_access)
def listar_vagas(request):
    """
    View para listar vagas disponíveis para alunos.
    """
    vagas = Vaga.objects.filter(ativa=True).order_by('-data_criacao')
    context = {'vagas': vagas}
    return render(request, 'vagas/listar.html', context)


@login_required
@user_passes_test(is_funcionairo_access)
def listar_usuarios(request):
    service = UsuarioService()
    tipo_filtro = request.GET.get('tipo')
    status_filtro = request.GET.get('status')

    ativo = None
    if status_filtro:
        ativo = (status_filtro == 'ativo')

    usuarios = service.list_users(tipo_id=tipo_filtro, ativo=ativo)

    context = {'usuarios': usuarios}
    return render(request, 'usuarios/listar.html', context)


def criar_usuario(request):
    service = UsuarioService()
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        tipo_usuario_id = request.POST.get('tipo_usuario')

        try:
            service.create_user(nome, email, tipo_usuario_id)
            return redirect('listar_usuarios')
        except Exception:
            pass

    tipos_usuario = TipoUsuario.objects.filter(ativo=True)
    context = {'tipos_usuario': tipos_usuario}
    return render(request, 'usuarios/criar.html', context)


@login_required
@user_passes_test(is_aluno_access)
def editar_usuario(request, usuario_id):
    service = UsuarioService()
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        ativo = request.POST.get('ativo') == 'on'
        service.update_user(usuario_id, nome=nome, email=email, ativo=ativo)
        return redirect('listar_usuarios')

    context = {'usuario': usuario}
    return render(request, 'usuarios/editar.html', context)

@login_required
@user_passes_test(is_adm)
def deletar_usuario(request, usuario_id):
    service = UsuarioService()
    nome = service.delete_user(usuario_id)
    return redirect('listar_usuarios')