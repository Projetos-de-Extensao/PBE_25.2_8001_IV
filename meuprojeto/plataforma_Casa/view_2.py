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

from .models import ParticipacaoMonitoria, Presenca, Sala, Turma, Vaga, Inscricao, Curso, Usuario, TipoUsuario

from .service import MonitoriaService, PerfilService, PortalVagasService, PresencaService, RelatorioService, TurmaService, VagaService, UsuarioService, AlunoService, Aluno

# Criado o VagaService para encapsular a lógica de negócio da view detalhe_vaga






@login_required
@user_passes_test(is_funcionairo_access)
def listar_monitorias(request):
    service = MonitoriaService()
    turma_filtro = request.GET.get('turma')
    context = service.listar_monitorias(request.user, turma_id=turma_filtro)
    return render(request, 'monitorias/listar.html', context)


@login_required
@user_passes_test(is_funcionairo_access or is_monitor_access)
def editar_participacao(request, participacao_id):
    service = MonitoriaService()
    participacao = get_object_or_404(ParticipacaoMonitoria, id=participacao_id)
    if request.method == 'POST':
        ap1 = request.POST.get('ap1') or None
        ap2 = request.POST.get('ap2') or None
        cr = request.POST.get('cr') or None
        service.editar_participacao(participacao_id, ap1=ap1, ap2=ap2, cr=cr)
        return redirect('listar_monitorias')
    context = {'participacao': participacao}
    return render(request, 'monitorias/editar.html', context)


@login_required
@user_passes_test(is_funcionairo_access or is_monitor_access)
def listar_presencas(request):
    service = PresencaService()
    turma_filtro = request.GET.get('turma')
    data_filtro = request.GET.get('data')
    context = service.listar_presencas(turma_id=turma_filtro, data=data_filtro)
    return render(request, 'presencas/listar.html', context)


@login_required
@user_passes_test(is_funcionairo_access or is_monitor_access)
def editar_presenca(request, presenca_id):
    service = PresencaService()
    presenca = get_object_or_404(Presenca, id=presenca_id)
    if request.method == 'POST':
        presente = request.POST.get('presente') == 'on'
        service.editar_presenca(presenca_id, presente)
        return redirect('listar_presencas')
    context = {'presenca': presenca}
    return render(request, 'presencas/editar.html', context)

### 8. MÓDULO DE RELATÓRIOS - ANÁLISE E CONSULTORIA
@login_required
@user_passes_test(is_funcionairo_access or is_monitor_access)
def listar_relatorios(request):
    return render(request, 'relatorios/listar.html')

@login_required
@user_passes_test(is_funcionairo_access or is_monitor_access)
def relatorio_desempenho(request):
    context = RelatorioService().desempenho()
    return render(request, 'relatorios/desempenho.html', context)

@login_required
@user_passes_test(is_funcionairo_access or is_monitor_access)
def relatorio_frequencia(request):
    context = RelatorioService().frequencia()
    return render(request, 'relatorios/frequencia.html', context)

@login_required
@user_passes_test(is_funcionairo_access or is_monitor_access)
def relatorio_inscricoes(request):
    context = RelatorioService().inscricoes()
    return render(request, 'relatorios/inscricoes.html', context)

@login_required
@user_passes_test(is_funcionairo_access or is_monitor_access)
def relatorio_geral(request):
    context = RelatorioService().geral()
    return render(request, 'relatorios/geral.html', context)



@login_required(login_url='login')
def perfil(request):
    service = PerfilService()
    if request.method == 'POST':
        service.atualizar_perfil(request.user, request.POST)
        # messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil')
    context = service.get_perfil_context(request.user)
    return render(request, 'perfil.html', context)



