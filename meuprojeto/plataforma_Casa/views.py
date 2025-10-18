from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count, Q, Avg
from .models import (
    Usuario, Aluno, Funcionario, Curso, Sala, Vaga, Turma, 
    ParticipacaoMonitoria, Presenca, Inscricao, TipoUsuario
)
from .repository import (
    listar_usuarios, listar_alunos, listar_cursos, listar_funcionarios, 
    listar_inscricoes, listar_turmas, listar_participacoes_monitoria, 
    listar_presencas, listar_salas, listar_tipos_usuario
)


# ==================== DASHBOARD ====================
def dashboard(request):
    """
    View do Dashboard - Página inicial com resumo geral
    """
    total_usuarios = Usuario.objects.filter(ativo=True).count()
    total_alunos = Aluno.objects.filter(ativo=True).count()
    total_turmas = Turma.objects.filter(ativo=True).count()
    total_vagas = Vaga.objects.filter(ativo=True).count()
    
    ultimas_monitorias = Turma.objects.filter(ativo=True).order_by('-criado_em')[:5]
    inscricoes_pendentes = Inscricao.objects.filter(status='Pendente')[:5]
    
    context = {
        'total_usuarios': total_usuarios,
        'total_alunos': total_alunos,
        'total_turmas': total_turmas,
        'total_vagas': total_vagas,
        'ultimas_monitorias': ultimas_monitorias,
        'inscricoes_pendentes': inscricoes_pendentes,
    }
    return render(request, 'dashboard.html', context)


# ==================== USUÁRIOS ====================
def listar_usuarios(request):
    """
    View para listar todos os usuários
    """
    usuarios = Usuario.objects.all().select_related('tipo_usuario')
    
    # Filtro por tipo de usuário
    tipo_filtro = request.GET.get('tipo')
    if tipo_filtro:
        usuarios = usuarios.filter(tipo_usuario__id=tipo_filtro)
    
    # Filtro por status
    status_filtro = request.GET.get('status')
    if status_filtro:
        usuarios = usuarios.filter(ativo=(status_filtro == 'ativo'))
    
    context = {
        'usuarios': usuarios,
    }
    return render(request, 'usuarios/listar.html', context)


def criar_usuario(request):
    """
    View para criar novo usuário
    """
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        tipo_usuario_id = request.POST.get('tipo_usuario')
        
        try:
            tipo_usuario = TipoUsuario.objects.get(id=tipo_usuario_id)
            usuario = Usuario.objects.create(
                nome=nome,
                email=email,
                tipo_usuario=tipo_usuario,
                ativo=True
            )
            messages.success(request, f'Usuário "{nome}" criado com sucesso!')
            return redirect('listar_usuarios')
        except Exception as e:
            messages.error(request, f'Erro ao criar usuário: {str(e)}')
    
    tipos_usuario = TipoUsuario.objects.filter(ativo=True)
    context = {'tipos_usuario': tipos_usuario}
    return render(request, 'usuarios/criar.html', context)


def editar_usuario(request, usuario_id):
    """
    View para editar usuário existente
    """
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    if request.method == 'POST':
        usuario.nome = request.POST.get('nome')
        usuario.email = request.POST.get('email')
        usuario.ativo = request.POST.get('ativo') == 'on'
        usuario.save()
        messages.success(request, 'Usuário atualizado com sucesso!')
        return redirect('listar_usuarios')
    
    context = {'usuario': usuario}
    return render(request, 'usuarios/editar.html', context)


def deletar_usuario(request, usuario_id):
    """
    View para deletar usuário
    """
    usuario = get_object_or_404(Usuario, id=usuario_id)
    nome = usuario.nome
    usuario.delete()
    messages.success(request, f'Usuário "{nome}" deletado com sucesso!')
    return redirect('listar_usuarios')


# ==================== ALUNOS ====================
def listar_alunos(request):
    """
    View para listar todos os alunos
    """
    alunos = Aluno.objects.all().select_related('curso', 'tipo_usuario')
    
    # Filtro por curso
    curso_filtro = request.GET.get('curso')
    if curso_filtro:
        alunos = alunos.filter(curso__id=curso_filtro)
    
    # Filtro por período
    periodo_filtro = request.GET.get('periodo')
    if periodo_filtro:
        alunos = alunos.filter(periodo=periodo_filtro)
    
    context = {
        'alunos': alunos,
        'cursos': Curso.objects.all(),
    }
    return render(request, 'alunos/listar.html', context)


def criar_aluno(request):
    """
    View para criar novo aluno
    """
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        matricula = request.POST.get('matricula')
        curso_id = request.POST.get('curso')
        periodo = request.POST.get('periodo')
        cr_geral = request.POST.get('cr_geral', 0)
        
        try:
            tipo_usuario = TipoUsuario.objects.get(tipo='aluno')
            curso = Curso.objects.get(id=curso_id)
            
            aluno = Aluno.objects.create(
                nome=nome,
                email=email,
                matricula=matricula,
                curso=curso,
                periodo=periodo,
                cr_geral=float(cr_geral),
                tipo_usuario=tipo_usuario,
                data_ingresso='2025-01-01',  # Ajuste conforme necessário
                ativo=True
            )
            messages.success(request, f'Aluno "{nome}" criado com sucesso!')
            return redirect('listar_alunos')
        except Exception as e:
            messages.error(request, f'Erro ao criar aluno: {str(e)}')
    
    context = {
        'cursos': Curso.objects.filter(ativo=True),
    }
    return render(request, 'alunos/criar.html', context)


def editar_aluno(request, aluno_id):
    """
    View para editar aluno
    """
    aluno = get_object_or_404(Aluno, id=aluno_id)
    
    if request.method == 'POST':
        aluno.nome = request.POST.get('nome')
        aluno.email = request.POST.get('email')
        aluno.periodo = request.POST.get('periodo')
        aluno.cr_geral = request.POST.get('cr_geral', aluno.cr_geral)
        aluno.ativo = request.POST.get('ativo') == 'on'
        aluno.save()
        messages.success(request, 'Aluno atualizado com sucesso!')
        return redirect('listar_alunos')
    
    context = {'aluno': aluno}
    return render(request, 'alunos/editar.html', context)


def deletar_aluno(request, aluno_id):
    """
    View para deletar aluno
    """
    aluno = get_object_or_404(Aluno, id=aluno_id)
    nome = aluno.nome
    aluno.delete()
    messages.success(request, f'Aluno "{nome}" deletado com sucesso!')
    return redirect('listar_alunos')


# ==================== VAGAS ====================
def listar_vagas(request):
    """
    View para listar todas as vagas
    """
    vagas = Vaga.objects.all().select_related('curso', 'coordenador').prefetch_related('monitores')
    
    # Filtro por curso
    curso_filtro = request.GET.get('curso')
    if curso_filtro:
        vagas = vagas.filter(curso__id=curso_filtro)
    
    # Filtro por status
    status_filtro = request.GET.get('status')
    if status_filtro:
        vagas = vagas.filter(ativo=(status_filtro == 'ativa'))
    
    context = {
        'vagas': vagas,
        'cursos': Curso.objects.all(),
    }
    return render(request, 'vagas/listar.html', context)


def detalhe_vaga(request, vaga_id):
    """
    View para detalhar uma vaga específica
    """
    vaga = get_object_or_404(Vaga, id=vaga_id)
    inscricoes = Inscricao.objects.filter(vaga=vaga).select_related('aluno')
    
    context = {
        'vaga': vaga,
        'inscricoes': inscricoes,
    }
    return render(request, 'vagas/detalhe.html', context)


def criar_vaga(request):
    """
    View para criar nova vaga
    """
    if request.method == 'POST':
        nome = request.POST.get('nome')
        curso_id = request.POST.get('curso')
        coordenador_id = request.POST.get('coordenador')
        descricao = request.POST.get('descricao')
        requisitos = request.POST.get('requisitos')
        
        try:
            curso = Curso.objects.get(id=curso_id)
            coordenador = Funcionario.objects.get(id=coordenador_id)
            
            vaga = Vaga.objects.create(
                nome=nome,
                curso=curso,
                coordenador=coordenador,
                descricao=descricao,
                requisitos=requisitos,
                ativo=True
            )
            messages.success(request, f'Vaga "{nome}" criada com sucesso!')
            return redirect('listar_vagas')
        except Exception as e:
            messages.error(request, f'Erro ao criar vaga: {str(e)}')
    
    context = {
        'cursos': Curso.objects.filter(ativo=True),
        'coordenadores': Funcionario.objects.filter(ativo=True, coordenador=True),
    }
    return render(request, 'vagas/criar.html', context)


def editar_vaga(request, vaga_id):
    """
    View para editar vaga
    """
    vaga = get_object_or_404(Vaga, id=vaga_id)
    
    if request.method == 'POST':
        vaga.nome = request.POST.get('nome')
        vaga.descricao = request.POST.get('descricao')
        vaga.requisitos = request.POST.get('requisitos')
        vaga.ativo = request.POST.get('ativo') == 'on'
        vaga.save()
        messages.success(request, 'Vaga atualizada com sucesso!')
        return redirect('listar_vagas')
    
    context = {'vaga': vaga}
    return render(request, 'vagas/editar.html', context)


def deletar_vaga(request, vaga_id):
    """
    View para deletar vaga
    """
    vaga = get_object_or_404(Vaga, id=vaga_id)
    nome = vaga.nome
    vaga.delete()
    messages.success(request, f'Vaga "{nome}" deletada com sucesso!')
    return redirect('listar_vagas')


# ==================== TURMAS ====================
def listar_turmas(request):
    """
    View para listar todas as turmas
    """
    turmas = Turma.objects.all().select_related('vaga', 'monitor', 'sala', 'curso')
    
    # Filtro por vaga
    vaga_filtro = request.GET.get('vaga')
    if vaga_filtro:
        turmas = turmas.filter(vaga__id=vaga_filtro)
    
    # Filtro por status
    status_filtro = request.GET.get('status')
    if status_filtro:
        turmas = turmas.filter(ativo=(status_filtro == 'ativa'))
    
    context = {
        'turmas': turmas,
        'vagas': Vaga.objects.all(),
    }
    return render(request, 'turmas/listar.html', context)


def detalhe_turma(request, turma_id):
    """
    View para detalhar uma turma específica
    """
    turma = get_object_or_404(Turma, id=turma_id)
    participacoes = ParticipacaoMonitoria.objects.filter(turma=turma).select_related('aluno')
    presencas = Presenca.objects.filter(turma=turma).select_related('aluno')
    
    context = {
        'turma': turma,
        'participacoes': participacoes,
        'presencas': presencas,
    }
    return render(request, 'turmas/detalhe.html', context)


def criar_turma(request):
    """
    View para criar nova turma
    """
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
            vaga = Vaga.objects.get(id=vaga_id)
            sala = Sala.objects.get(id=sala_id)
            monitor = Aluno.objects.get(id=monitor_id)
            curso = Curso.objects.get(id=curso_id)
            
            turma = Turma.objects.create(
                nome=nome,
                vaga=vaga,
                sala=sala,
                descricao=descricao,
                data_inicio=data_inicio,
                data_fim=data_fim,
                dias_da_semana=dias_semana,
                horario=horario,
                monitor=monitor,
                curso=curso,
                ativo=True
            )
            messages.success(request, f'Turma "{nome}" criada com sucesso!')
            return redirect('listar_turmas')
        except Exception as e:
            messages.error(request, f'Erro ao criar turma: {str(e)}')
    
    context = {
        'vagas': Vaga.objects.filter(ativo=True),
        'salas': Sala.objects.filter(ativo=True),
        'monitores': Aluno.objects.filter(ativo=True),
        'cursos': Curso.objects.filter(ativo=True),
    }
    return render(request, 'turmas/criar.html', context)


def editar_turma(request, turma_id):
    """
    View para editar turma
    """
    turma = get_object_or_404(Turma, id=turma_id)
    
    if request.method == 'POST':
        turma.nome = request.POST.get('nome')
        turma.descricao = request.POST.get('descricao')
        turma.horario = request.POST.get('horario')
        turma.ativo = request.POST.get('ativo') == 'on'
        turma.save()
        messages.success(request, 'Turma atualizada com sucesso!')
        return redirect('listar_turmas')
    
    context = {'turma': turma}
    return render(request, 'turmas/editar.html', context)


def deletar_turma(request, turma_id):
    """
    View para deletar turma
    """
    turma = get_object_or_404(Turma, id=turma_id)
    nome = turma.nome
    turma.delete()
    messages.success(request, f'Turma "{nome}" deletada com sucesso!')
    return redirect('listar_turmas')


# ==================== MONITORIAS ====================
def listar_monitorias(request):
    """
    View para listar participações em monitorias
    """
    participacoes = ParticipacaoMonitoria.objects.all().select_related('aluno', 'turma')
    turmas = Turma.objects.filter(ativo=True)
    
    # Filtro por turma
    turma_filtro = request.GET.get('turma')
    if turma_filtro:
        participacoes = participacoes.filter(turma__id=turma_filtro)
    
    context = {
        'participacoes': participacoes,
        'turmas': turmas,
    }
    return render(request, 'monitorias/listar.html', context)


def editar_participacao(request, participacao_id):
    """
    View para editar participação em monitoria
    """
    participacao = get_object_or_404(ParticipacaoMonitoria, id=participacao_id)
    
    if request.method == 'POST':
        participacao.ap1 = request.POST.get('ap1') or None
        participacao.ap2 = request.POST.get('ap2') or None
        participacao.cr = request.POST.get('cr') or None
        participacao.save()
        messages.success(request, 'Participação atualizada com sucesso!')
        return redirect('listar_monitorias')
    
    context = {'participacao': participacao}
    return render(request, 'monitorias/editar.html', context)


# ==================== PRESENÇAS ====================
def listar_presencas(request):
    """
    View para listar presenças
    """
    presencas = Presenca.objects.all().select_related('aluno', 'turma')
    turmas = Turma.objects.filter(ativo=True)
    
    # Filtro por turma
    turma_filtro = request.GET.get('turma')
    if turma_filtro:
        presencas = presencas.filter(turma__id=turma_filtro)
    
    # Filtro por data
    data_filtro = request.GET.get('data')
    if data_filtro:
        presencas = presencas.filter(data=data_filtro)
    
    context = {
        'presencas': presencas,
        'turmas': turmas,
    }
    return render(request, 'presencas/listar.html', context)


def editar_presenca(request, presenca_id):
    """
    View para editar presença
    """
    presenca = get_object_or_404(Presenca, id=presenca_id)
    
    if request.method == 'POST':
        presenca.presente = request.POST.get('presente') == 'on'
        presenca.save()
        messages.success(request, 'Presença atualizada com sucesso!')
        return redirect('listar_presencas')
    
    context = {'presenca': presenca}
    return render(request, 'presencas/editar.html', context)


# ==================== RELATÓRIOS ====================
def listar_relatorios(request):
    """
    View para listar relatórios disponíveis
    """
    return render(request, 'relatorios/listar.html')


def relatorio_desempenho(request):
    """
    View para gerar relatório de desempenho
    """
    participacoes = ParticipacaoMonitoria.objects.all().select_related('aluno', 'turma')
    
    context = {
        'participacoes': participacoes,
        'titulo': 'Relatório de Desempenho',
    }
    return render(request, 'relatorios/desempenho.html', context)


def relatorio_frequencia(request):
    """
    View para gerar relatório de frequência
    """
    presencas = Presenca.objects.all().select_related('aluno', 'turma')
    
    context = {
        'presencas': presencas,
        'titulo': 'Relatório de Frequência',
    }
    return render(request, 'relatorios/frequencia.html', context)


def relatorio_inscricoes(request):
    """
    View para gerar relatório de inscrições
    """
    inscricoes = Inscricao.objects.all().select_related('aluno', 'vaga')
    
    context = {
        'inscricoes': inscricoes,
        'titulo': 'Relatório de Inscrições',
    }
    return render(request, 'relatorios/inscricoes.html', context)


def relatorio_geral(request):
    """
    View para gerar relatório geral
    """
    total_usuarios = Usuario.objects.filter(ativo=True).count()
    total_alunos = Aluno.objects.filter(ativo=True).count()
    total_funcionarios = Funcionario.objects.filter(ativo=True).count()
    total_turmas = Turma.objects.filter(ativo=True).count()
    total_vagas = Vaga.objects.filter(ativo=True).count()
    total_inscricoes = Inscricao.objects.count()
    total_presencas = Presenca.objects.filter(presente=True).count()
    
    context = {
        'total_usuarios': total_usuarios,
        'total_alunos': total_alunos,
        'total_funcionarios': total_funcionarios,
        'total_turmas': total_turmas,
        'total_vagas': total_vagas,
        'total_inscricoes': total_inscricoes,
        'total_presencas': total_presencas,
        'titulo': 'Relatório Geral',
    }
    return render(request, 'relatorios/geral.html', context)


# ==================== PERFIL ====================
def perfil(request):
    """
    View para exibir e editar perfil do usuário
    """
    usuario = request.user
    
    if request.method == 'POST':
        usuario.first_name = request.POST.get('nome')
        usuario.email = request.POST.get('email')
        usuario.save()
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil')
    
    context = {'usuario': usuario}
    return render(request, 'perfil.html', context)


def alterar_senha(request):
    """
    View para alterar senha do usuário
    """
    if request.method == 'POST':
        senha_nova = request.POST.get('senha_nova')
        senha_confirmar = request.POST.get('senha_confirmar')
        
        if senha_nova == senha_confirmar:
            request.user.set_password(senha_nova)
            request.user.save()
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('perfil')
        else:
            messages.error(request, 'As senhas não coincidem!')
            return redirect('perfil')
    
    return redirect('perfil')


# ==================== VIEW SQL (ORIGINAL) ====================
def sql_view(request):
    """
    View original - Exibe dados SQL em template
    """
    usuarios = listar_usuarios()
    alunos = listar_alunos()
    cursos = listar_cursos()
    funcionarios = listar_funcionarios()
    inscricoes = listar_inscricoes()
    turmas = listar_turmas()
    participacoes_monitoria = listar_participacoes_monitoria()
    presencas = listar_presencas()
    salas = listar_salas()
    tipos_usuario = listar_tipos_usuario()
    
    return render(request, 'sql_template.html', {
        'usuarios': usuarios, 
        'alunos': alunos, 
        'cursos': cursos, 
        'funcionarios': funcionarios, 
        'inscricoes': inscricoes, 
        'turmas': turmas, 
        'participacoes_monitoria': participacoes_monitoria, 
        'presencas': presencas, 
        'salas': salas, 
        'tipos_usuario': tipos_usuario
    })
