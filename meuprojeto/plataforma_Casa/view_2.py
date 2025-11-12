from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib import messages
from .permission import (
            is_adm, 
            is_admin_user, 
            is_aluno_access, 
            is_monitor_access, 
            is_funcionairo_access
            )

from .models import Sala, Turma, Vaga, Inscricao, Curso, Usuario, TipoUsuario

from .service import TurmaService, VagaService, UsuarioService, AlunoService, Aluno

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


@login_required
@user_passes_test(is_aluno_access)
def listar_alunos(request):
    service = AlunoService()
    curso_filtro = request.GET.get('curso')
    periodo_filtro = request.GET.get('periodo')

    alunos = service.list_alunos(curso_id=curso_filtro, periodo=periodo_filtro)

    context = {
        'alunos': alunos,
        'cursos': Curso.objects.all(),
    }
    return render(request, 'alunos/listar.html', context)


@login_required
@user_passes_test(is_aluno_access )
def criar_aluno(request):
    service = AlunoService()
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        matricula = request.POST.get('matricula')
        curso_id = request.POST.get('curso')
        periodo = request.POST.get('periodo')
        cr_geral = request.POST.get('cr_geral', 0)

        try:
            service.create_aluno(nome, email, matricula, curso_id, periodo=periodo, cr_geral=cr_geral)
            return redirect('listar_alunos')
        except Exception as e:
            messages.error(request, f'Erro ao criar aluno: {e}')

    context = {
        'cursos': Curso.objects.filter(ativo=True),
    }
    return render(request, 'alunos/criar.html', context)


@login_required
@user_passes_test(is_funcionairo_access or is_monitor_access) 
def editar_aluno(request, aluno_id):
    service = AlunoService()
    aluno = get_object_or_404(Aluno, id=aluno_id)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        periodo = request.POST.get('periodo')
        cr_geral = request.POST.get('cr_geral', aluno.cr_geral)
        ativo = request.POST.get('ativo') == 'on'

        try:
            service.update_aluno(aluno_id, nome=nome, email=email, periodo=periodo, cr_geral=cr_geral, ativo=ativo)
            return redirect('listar_alunos')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar aluno: {e}')

    context = {'aluno': aluno}
    return render(request, 'alunos/editar.html', context)


@login_required
@user_passes_test(is_funcionairo_access)
def deletar_aluno(request, aluno_id):
    service = AlunoService()
    try:
        service.delete_aluno(aluno_id)
    except Exception as e:
        messages.error(request, f'Erro ao deletar aluno: {e}')
    return redirect('listar_alunos')



@login_required
@user_passes_test(is_funcionairo_access or is_monitor_access)
def listar_turmas(request):
    service = TurmaService()
    vaga_filtro = request.GET.get('vaga')
    status_filtro = request.GET.get('status')
    turmas = service.list_turmas(vaga_id=vaga_filtro, status=status_filtro)
    context = {
        'turmas': turmas,
        'vagas': Vaga.objects.all(),
    }
    return render(request, 'turmas/listar.html', context)

@login_required
@user_passes_test(is_funcionairo_access or is_monitor_access)
def detalhe_turma(request, turma_id):
    service = TurmaService()
    context = service.get_turma_detail(turma_id)
    return render(request, 'turmas/detalhe.html', context)

@login_required
@user_passes_test(is_funcionairo_access or is_monitor_access)
def criar_turma(request):
    service = TurmaService()
    if request.method == 'POST':
        nome = request.POST.get('nome')
        vaga_id = request.POST.get('vaga')
        sala_id = request.POST.get('sala')
        descricao = request.POST.get('descricao')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        dias_semana = request.POST.get('dias_semana')
        horario = request.POST.get('horario')
        monitor_id = request.POST.get('monitor')
        curso_id = request.POST.get('curso')
        try:
            service.create_turma(nome, vaga_id, sala_id, descricao, data_inicio, data_fim, dias_semana, horario, monitor_id, curso_id)
            return redirect('listar_turmas')
        except Exception as e:
            pass
    context = {
        'vagas': Vaga.objects.filter(ativo=True),
        'salas': Sala.objects.filter(ativo=True),
        'monitores': Aluno.objects.filter(ativo=True),
        'cursos': Curso.objects.filter(ativo=True),
    }
    return render(request, 'turmas/criar.html', context)

@login_required
@user_passes_test(is_funcionairo_access or is_monitor_access)
def editar_turma(request, turma_id):
    service = TurmaService()
    turma = get_object_or_404(Turma, id=turma_id)
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        horario = request.POST.get('horario')
        ativo = request.POST.get('ativo') == 'on'
        service.update_turma(turma_id, nome=nome, descricao=descricao, horario=horario, ativo=ativo)
        return redirect('listar_turmas')
    context = {'turma': turma}
    return render(request, 'turmas/editar.html', context)

@login_required
@user_passes_test(is_funcionairo_access or is_monitor_access)
def deletar_turma(request, turma_id):
    service = TurmaService()
    service.delete_turma(turma_id)
    return redirect('listar_turmas')


