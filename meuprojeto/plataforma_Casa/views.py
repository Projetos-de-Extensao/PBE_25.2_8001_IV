from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth import login
from django.contrib import messages
from .permission import (
            is_adm, 
            is_admin_user, 
            is_aluno_access, 
            is_monitor_access, 
            is_funcionairo_access,
            is_professor_access
            )

from .models import (
    Disciplina, 
    Funcionario, 
    ParticipacaoMonitoria, 
    Presenca,
    RegistroHoras,
    Aluno, 
    Sala, 
    Turma, 
    Vaga, 
    Inscricao, 
    Curso, 
    Usuario, 
    TipoUsuario
)

from .service import (
    AuthService,
    DashboardGestaoService,
    DisciplinaService,
    MonitoriaService,
    PagamentoService, 
    PerfilService, 
    PortalVagasService, 
    PresencaService,
    RegistroHorasService,
    RegistroService, 
    RelatorioService, 
    TurmaService, 
    VagaMonitoriaService, 
    VagaMonitoriaService, 
    VagaService, 
    UsuarioService, 
    AlunoService
    )

from .forms import DisciplinaForm


from django.contrib.auth import login, get_user_model


def login_view(request):
    """
    View de Login - Autentica usuários com username ou email
    Backend customizado (EmailOrUsernameModelBackend) permite ambos
    """
    service = AuthService()
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = service.autenticar_usuario(request, username, password)
        if user is not None:
            login(request, user)
            
            # Lógica de redirecionamento por grupo
            if user.groups.filter(name='Aluno').exists():
                # Se for Aluno, verifica se também é Monitor
                if user.groups.filter(name='Monitor').exists():
                    return redirect('dashboard_monitor')
                return redirect('portal_vagas')
            elif user.groups.filter(name='Professor').exists():
                return redirect('dashboard_professor') # Rota que vamos criar
            elif user.groups.filter(name__in=['Admin', 'Coordenador']).exists():
                return redirect('dashboard_gestao')
            else:
                # Um fallback, caso o usuário não tenha um grupo esperado
                return redirect('home') 
                
        else:
            messages.error(request, 'Usuário ou senha inválidos!')
    return render(request, 'login.html')

def logout_view(request):
    """
    View de Logout - Faz logout do usuário
    """
    AuthService().logout(request)
    return redirect('login')


def register_view(request):
    service = RegistroService()
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip()
        matricula = request.POST.get('matricula', '').strip()
        curso_id = request.POST.get('curso')
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        terms = request.POST.get('terms')
        erros = service.validar_dados(nome, email, matricula, curso_id, password, password_confirm, terms)
        if erros:
            for erro in erros:
                messages.error(request, f'❌ {erro}')
            return redirect('register')
        try:
            user, aluno = service.registrar_usuario_aluno(nome, email, matricula, curso_id, password)
            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'❌ Erro ao registrar: {str(e)}')
            return redirect('register')
    cursos = RegistroService.get_cursos_ativos()
    context = {'cursos': cursos}
    return render(request, 'register.html', context)



##### 2. MÓDULO DE USUÁRIOS - CRUD COMPLETO ### 
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

##### 3. MÓDULO DE ALUNOS - CRUD COMPLETO ###
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


### 5. MÓDULO DE TURMAS - CRUD + DETALHE
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


## 4. MÓDULO DE VAGAS - CRUD + DETALHE 
@login_required
def listar_vagas_monitoria(request):
    service = VagaMonitoriaService()
    curso_filtro = request.GET.get('curso')
    status_filtro = request.GET.get('status')
    vagas = service.listar_vagas(request.user, curso_filtro, status_filtro)
    context = {
        'vagas': vagas,
        'cursos': Curso.objects.filter(ativo=True),
    }
    return render(request, 'monitorias/disponiveis.html', context)

@login_required
def detalhe_vaga_monitoria(request, vaga_id):
    service = VagaMonitoriaService()
    result = service.detalhe_vaga(vaga_id, request.user)
    if not result:
        messages.error(request, 'Você não tem permissão para acessar esta vaga.')
        return redirect('listar_vagas_monitoria')
    context = result
    return render(request, 'monitorias/detalhe.html', context)

@login_required
def criar_vaga_monitoria(request):
    service = VagaMonitoriaService()
    if request.method == 'POST':
        nome = request.POST.get('nome')
        curso_id = request.POST.get('curso')
        disciplina_id = request.POST.get('disciplina')
        coordenador_id = request.POST.get('coordenador')
        descricao = request.POST.get('descricao')
        requisitos = request.POST.get('requisitos')
        numero_vagas = request.POST.get('numero_vagas')
        vaga = service.criar_vaga(nome, curso_id, disciplina_id, coordenador_id, descricao, requisitos, numero_vagas, request.user)
        if vaga:
            messages.success(request, 'Vaga criada com sucesso!')
            return redirect('listar_vagas_monitoria')
        else:
            messages.error(request, 'Erro ao criar vaga ou permissão negada.')
    context = {
        'cursos': Curso.objects.filter(ativo=True),
        'disciplinas': Disciplina.objects.filter(ativo=True),
        'coordenadores': Funcionario.objects.filter(ativo=True, coordenador=True),
    }
    return render(request, 'monitorias/criar.html', context)

@login_required
def editar_vaga_monitoria(request, vaga_id):
    service = VagaMonitoriaService()
    vaga = get_object_or_404(Vaga, id=vaga_id)
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        requisitos = request.POST.get('requisitos')
        ativo = request.POST.get('ativo') == 'on'
        coordenadores_ids = request.POST.getlist('coordenadores')
        professores_ids = request.POST.getlist('professores')
        vaga_editada = service.editar_vaga(vaga_id, request.user, nome, descricao, requisitos, ativo, coordenadores_ids, professores_ids)
        if vaga_editada:
            messages.success(request, 'Vaga editada com sucesso!')
            return redirect('listar_vagas_monitoria')
        else:
            messages.error(request, 'Erro ao editar vaga ou permissão negada.')
    context = {
        'vaga': vaga,
        'coordenadores': Funcionario.objects.filter(coordenador=True),
        'professores': Funcionario.objects.filter(funcao='Professor'),
    }
    return render(request, 'monitorias/editar.html', context)

@login_required
def deletar_vaga_monitoria(request, vaga_id):
    service = VagaMonitoriaService()
    nome = service.deletar_vaga(vaga_id, request.user)
    if nome:
        messages.success(request, f'Vaga "{nome}" deletada com sucesso!')
    else:
        messages.error(request, 'Erro ao deletar vaga ou permissão negada.')
    return redirect('listar_vagas_monitoria')


## 5. MÓDULO DE TURMAS - CRUD + DETALHE
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
@login_required
def listar_turmas(request):
    service = TurmaService()
    vaga_filtro = request.GET.get('vaga')
    status_filtro = request.GET.get('status')
    turmas = service.listar_turmas(vaga_filtro, status_filtro)
    context = {
        'turmas': turmas,
        'vagas': Vaga.objects.all(),
    }
    return render(request, 'turmas/listar.html', context)

@user_passes_test(lambda u: u.is_staff or u.is_superuser)
@login_required
def detalhe_turma(request, turma_id):
    service = TurmaService()
    context = service.detalhe_turma(turma_id)
    return render(request, 'turmas/detalhe.html', context)

@user_passes_test(lambda u: u.is_staff or u.is_superuser)
@login_required
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
        turma = service.criar_turma(nome, vaga_id, sala_id, descricao, data_inicio, data_fim, dias_semana, horario, monitor_id, curso_id)
        if turma:
            messages.success(request, f'Turma "{nome}" criada com sucesso!')
            return redirect('listar_turmas')
        else:
            messages.error(request, 'Erro ao criar turma.')
    context = {
        'vagas': Vaga.objects.filter(ativo=True),
        'salas': Sala.objects.filter(ativo=True),
        'monitores': Aluno.objects.filter(ativo=True),
        'cursos': Curso.objects.filter(ativo=True),
    }
    return render(request, 'turmas/criar.html', context)

@user_passes_test(lambda u: u.is_staff or u.is_superuser)
@login_required
def editar_turma(request, turma_id):
    service = TurmaService()
    turma = get_object_or_404(Turma, id=turma_id)
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        horario = request.POST.get('horario')
        ativo = request.POST.get('ativo') == 'on'
        turma_editada = service.editar_turma(turma_id, nome, descricao, horario, ativo)
        if turma_editada:
            messages.success(request, 'Turma atualizada com sucesso!')
            return redirect('listar_turmas')
        else:
            messages.error(request, 'Erro ao atualizar turma.')
    context = {'turma': turma}
    return render(request, 'turmas/editar.html', context)

@user_passes_test(lambda u: u.is_staff or u.is_superuser)
@login_required
def deletar_turma(request, turma_id):
    service = TurmaService()
    nome = service.deletar_turma(turma_id)
    if nome:
        messages.success(request, f'Turma "{nome}" deletada com sucesso!')
    else:
        messages.error(request, 'Erro ao deletar turma.')
    return redirect('listar_turmas')

## 8. MÓDULO DE RELATÓRIOS - ANÁLISE E CONSULTORIA
@login_required
def listar_relatorios(request):
    return render(request, 'relatorios/listar.html')

@login_required
def relatorio_desempenho(request):
    service = RelatorioService()
    context = service.desempenho()
    return render(request, 'relatorios/desempenho.html', context)

@login_required
def relatorio_frequencia(request):
    service = RelatorioService()
    context = service.frequencia()
    return render(request, 'relatorios/frequencia.html', context)

@login_required
def relatorio_inscricoes(request):
    service = RelatorioService()
    context = service.inscricoes()
    return render(request, 'relatorios/inscricoes.html', context)

@login_required
def relatorio_geral(request):
    service = RelatorioService()
    context = service.geral()
    return render(request, 'relatorios/geral.html', context)


@login_required
def portal_vagas(request):
    service = PortalVagasService()
    busca = request.GET.get('busca', '').strip()
    curso_filtro = request.GET.get('curso')
    tipo_filtro = request.GET.get('tipo')
    vagas = service.listar_vagas(busca, curso_filtro, tipo_filtro)
    stats = service.estatisticas()
    context = {
        'vagas': vagas,
        **stats,
    }
    if request.user.is_authenticated:
        aluno = service.get_aluno(request.user.email)
        context['aluno'] = aluno
        perfil_incompleto = request.session.pop('perfil_incompleto', None)
        vaga_tentada = request.session.pop('vaga_tentada', None)
        if perfil_incompleto:
            context['perfil_incompleto'] = perfil_incompleto
        if vaga_tentada:
            context['vaga_tentada'] = vaga_tentada
    template = 'vagas/portal_logged.html' if request.user.is_authenticated else 'vagas/portal_landing.html'
    return render(request, template, context)


## 11. PORTAL DE VAGAS E CANDIDATURAS
@login_required(login_url='login')
def candidatar_vaga(request, vaga_id):
    service = PortalVagasService()
    vaga = service.get_vaga(vaga_id)
    aluno = service.get_aluno(request.user.email)
    if not aluno:
        messages.error(request, '❌ Apenas alunos podem se candidatar a vagas de monitoria!')
        return redirect('portal_vagas')
    perfil_incompleto = service.pode_candidatar(aluno, vaga)
    if perfil_incompleto:
        request.session['perfil_incompleto'] = perfil_incompleto
        request.session['vaga_tentada'] = vaga_id
        messages.warning(request, '⚠️ Complete seu perfil para se candidatar a esta vaga!')
        return redirect('portal_vagas')
    if service.inscricao_exists(aluno, vaga):
        messages.warning(request, '⚠️ Você já se candidatou a esta vaga!')
        return redirect('minhas_inscricoes')
    if service.vagas_disponiveis(vaga) <= 0:
        messages.error(request, '❌ Esta vaga não possui mais vagas disponíveis.')
        return redirect('portal_vagas')
    if request.method == 'POST':
        inscricao, erro = service.candidatar(aluno, vaga, request.FILES)
        if inscricao:
            messages.success(request, f'✅ Candidatura enviada com sucesso para a vaga de {vaga.disciplina.nome}!')
            return redirect('minhas_inscricoes')
        else:
            messages.error(request, f'❌ Erro ao processar candidatura: {erro}')
    context = {'vaga': vaga, 'aluno': aluno}
    return render(request, 'vagas/candidatar.html', context)




# 13. REGISTRO E VALIDAÇÃO DE HORAS
@login_required
@user_passes_test(is_monitor_access)
def registrar_horas(request):
    service = RegistroHorasService()
    try:
        aluno = service.get_monitor_by_email(request.user.email)
        if not aluno:
            raise Exception("Monitor não encontrado")
        turmas = service.get_turmas_do_monitor(aluno)
    except Exception:
        if request.user.groups.filter(name='Aluno').exists():
            return redirect('portal_vagas')
        else:
            return redirect('dashboard')

    if request.method == 'POST':
        from datetime import datetime
        turma_id = request.POST.get('turma')
        data_str = request.POST.get('data')
        hora_inicio_str = request.POST.get('hora_inicio')
        hora_fim_str = request.POST.get('hora_fim')
        descricao = request.POST.get('descricao_atividade')
        try:
            data = datetime.strptime(data_str, '%Y-%m-%d').date()
            hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M').time()
            hora_fim = datetime.strptime(hora_fim_str, '%H:%M').time()
            if hora_fim <= hora_inicio:
                messages.error(request, '❌ Hora de fim deve ser maior que a hora de início.')
                context = {'turmas': turmas}
                return render(request, 'horas/registrar.html', context)
            service.criar_registro(turma_id, aluno, data, hora_inicio, hora_fim, descricao)
            return redirect('meus_registros_horas')
        except Turma.DoesNotExist:
            messages.error(request, '❌ Turma não encontrada ou você não é o monitor dela.')
        except ValueError:
            messages.error(request, '❌ Formato de data/hora inválido. Use formatos: data (YYYY-MM-DD), horário (HH:MM).')
        except Exception as e:
            messages.error(request, f'❌ Erro ao registrar horas: {str(e)}')

    context = {'turmas': turmas}
    return render(request, 'horas/registrar.html', context)


@login_required
@user_passes_test(is_professor_access)
def meus_registros_horas(request):
    service = RegistroHorasService()
    try:
        aluno = service.get_monitor_by_email(request.user.email)
        if not aluno:
            registros = []
        else:
            registros = service.get_registros_do_monitor(aluno)
    except Exception:
        registros = []
    context = {'registros': registros}
    return render(request, 'horas/meus_registros.html', context)

@login_required
@user_passes_test(is_professor_access)
def detalhes_registro(request, registro_id):
    service = RegistroHorasService()
    try:
        aluno = service.get_monitor_by_email(request.user.email)
        if not aluno:
            raise Exception("Monitor não encontrado")
        registro = service.get_registro_by_id_monitor(registro_id, aluno)
    except RegistroHoras.DoesNotExist:
        messages.error(request, '❌ Registro não encontrado ou você não tem permissão para acessá-lo.')
        return redirect('meus_registros_horas')
    except Exception:
        messages.error(request, '❌ Acesso negado: Você não é um monitor registrado.')
        return redirect('portal_vagas')
    context = {'registro': registro}
    return render(request, 'horas/detalhes_registro.html', context)


@login_required
@user_passes_test(is_professor_access)
def validar_horas(request):
    service = RegistroHorasService()
    try:
        registros = service.get_registros_pendentes()
    except Exception:
        registros = []
    context = {'registros': registros}
    return render(request, 'horas/validar.html', context)

@login_required
@user_passes_test(is_professor_access)
def aprovar_horas(request, registro_id):
    service = RegistroHorasService()
    registro = service.get_registro_by_id(registro_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        observacao = request.POST.get('observacao')
        try:
            funcionario = service.get_funcionario_by_email(request.user.email)
            service.aprovar_registro(registro, funcionario, status, observacao)
        except Exception:
            pass
        return redirect('validar_horas')
    context = {'registro': registro}
    return render(request, 'horas/aprovar.html', context)


# 14. DASHBOARD DE GESTÃO
@login_required
@user_passes_test(is_funcionairo_access)
def dashboard_gestao(request):
    """
    Dashboard com análises completas do sistema (perfil admin)
    ⚠️ APENAS ADMINS OU COORDENADORES podem acessar
    """
    try:
        context = DashboardGestaoService().get_dashboard_context()
        return render(request, 'gestao/dashboard.html', context)
    except Exception as e:
        import traceback
        from django.contrib import messages
        messages.error(request, f'Erro ao carregar dashboard de gestão: {str(e)}')
        print(f"ERRO DASHBOARD_GESTAO: {str(e)}")
        print(traceback.format_exc())
        return redirect('plataforma_Casa:dashboard')
    

# 16. GERENCIAMENTO DE DISCIPLINAS (PROFESSOR)

@login_required
@user_passes_test(is_funcionairo_access)
def listar_disciplinas(request):
    service = DisciplinaService()
    curso_filtro = request.GET.get('curso', '')
    periodo_filtro = request.GET.get('periodo', '')
    busca = request.GET.get('busca', '')
    disciplinas = service.listar_disciplinas(
        curso=curso_filtro or None,
        periodo=periodo_filtro or None,
        busca=busca or None
    )
    cursos = service.get_cursos_ativos()
    periodos = range(1, 11)
    context = {
        'disciplinas': disciplinas,
        'cursos': cursos,
        'periodos': periodos,
        'filtros': {
            'curso': curso_filtro,
            'periodo': periodo_filtro,
            'busca': busca,
        }
    }
    return render(request, 'professor/disciplinas/listar.html', context)

@login_required
@user_passes_test(is_funcionairo_access)
def criar_disciplina(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            try:
                disciplina = form.save(commit=False)
                from .models import Funcionario
                try:
                    funcionario = Funcionario.objects.get(email=request.user.email)
                    disciplina.criado_por = funcionario
                except Funcionario.DoesNotExist:
                    pass
                disciplina.save()
                form.save_m2m()
                messages.success(request, f'Disciplina "{disciplina.nome}" criada com sucesso!')
                return redirect('listar_disciplinas')
            except Exception as e:
                messages.error(request, f'Erro ao criar disciplina: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label}: {error}')
    else:
        form = DisciplinaForm()
    context = {
        'form': form,
        'title': 'Nova Disciplina',
    }
    return render(request, 'professor/disciplinas/criar.html', context)

@login_required
@user_passes_test(is_funcionairo_access)
def editar_disciplina(request, disciplina_id):
    service = DisciplinaService()
    try:
        disciplina = service.get_disciplina(disciplina_id)
        pode_editar = service.pode_editar(disciplina, request.user)
        if not pode_editar:
            messages.error(request, 'Você só pode editar disciplinas que você criou.')
            return redirect('listar_disciplinas')
        if request.method == 'POST':
            form = DisciplinaForm(request.POST, instance=disciplina)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, f'Disciplina "{disciplina.nome}" atualizada com sucesso!')
                    return redirect('listar_disciplinas')
                except Exception as e:
                    messages.error(request, f'Erro ao atualizar disciplina: {str(e)}')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{form.fields[field].label}: {error}')
        else:
            form = DisciplinaForm(instance=disciplina)
        context = {
            'form': form,
            'disciplina': disciplina,
            'title': f'Editar - {disciplina.nome}',
        }
        return render(request, 'professor/disciplinas/editar.html', context)
    except Exception as e:
        messages.error(request, f'Erro ao carregar disciplina: {str(e)}')
        return redirect('listar_disciplinas')
    
@login_required
@user_passes_test(is_funcionairo_access)
def detalhes_disciplina(request, disciplina_id):
    service = DisciplinaService()
    try:
        disciplina = service.get_disciplina(disciplina_id)
        vagas = disciplina.vagas.filter(ativo=True).order_by('-criado_em')
        total_vagas = vagas.count()
        total_inscritos = sum(vaga.inscricao_set.count() for vaga in vagas)
        context = {
            'disciplina': disciplina,
            'vagas': vagas,
            'total_vagas': total_vagas,
            'total_inscritos': total_inscritos,
        }
        return render(request, 'professor/disciplinas/detalhes.html', context)
    except Exception as e:
        messages.error(request, f'Erro ao carregar disciplina: {str(e)}')
        return redirect('listar_disciplinas')


@login_required
@user_passes_test(is_funcionairo_access)
def gerenciar_pagamentos(request):
    """
    View para gerenciar pagamentos dos monitores
    """
    service = PagamentoService()
    status_filtro = request.GET.get('status')
    pagamentos = service.listar_pagamentos(status=status_filtro)
    context = {'pagamentos': pagamentos}
    return render(request, 'gestao/pagamentos.html', context)


@login_required
@user_passes_test(is_funcionairo_access)
def processar_pagamento(request, pagamento_id):
    """
    View para processar um pagamento
    """
    service = PagamentoService()
    pagamento = service.obter_pagamento(pagamento_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        observacao = request.POST.get('observacao')
        try:
            service.processar_pagamento(
                pagamento_id=pagamento_id,
                status=status,
                observacao=observacao,
                processado_por_email=request.user.email
            )
        except Exception:
            # silêncio (mensagens podem ser adicionadas se desejar)
            pass
        return redirect('gerenciar_pagamentos')

    context = {'pagamento': pagamento}
    return render(request, 'gestao/processar_pagamento.html', context)

@login_required
@user_passes_test(is_professor_access)
def dashboard_professor(request):
    """
    Dashboard do Professor — usa template dashboard.html.
    """
    # Substitua pelo service adequado se existir (ex: ProfessorDashboardService)
    context = {
        'is_professor_dashboard': True
    }
    return render(request, 'dashboard.html', context)


@login_required
@user_passes_test(is_monitor_access)
def dashboard_monitor(request):
    """
    Dashboard do Monitor — mostra turmas e registros relacionados ao monitor.
    Rota acessível apenas para usuários com permissão de monitor.
    """
    service = RegistroHorasService()
    try:
        monitor = service.get_monitor_by_email(request.user.email)
        if not monitor:
            messages.error(request, 'Monitor não encontrado.')
            return redirect('portal_vagas')
        turmas = service.get_turmas_do_monitor(monitor)
        # tenta buscar registros do monitor, pode retornar []
        registros = []
        if hasattr(service, 'get_registros_do_monitor'):
            registros = service.get_registros_do_monitor(monitor)
    except Exception:
        messages.error(request, 'Erro ao carregar dados do dashboard do monitor.')
        return redirect('portal_vagas')

    context = {
        'is_monitor_dashboard': True,
        'turmas': turmas,
        'registros': registros,
    }
    return render(request, 'dashboard.html', context)



@login_required
def dashboard(request):
    """
    Rota genérica `dashboard` usada em templates como link "Home".
    Redireciona o usuário para o dashboard apropriado conforme seu grupo.
    """
    user = request.user
    # Admin / Coordenador -> dashboard de gestão
    if user.groups.filter(name__in=['Admin', 'Coordenador']).exists():
        return redirect('dashboard_gestao')
    # Professor -> dashboard do professor
    if user.groups.filter(name='Professor').exists():
        return redirect('dashboard_professor')
    # Monitor -> dashboard do monitor
    if user.groups.filter(name='Monitor').exists():
        return redirect('dashboard_monitor')
    # Aluno -> portal de vagas (página inicial para alunos)
    if user.groups.filter(name='Aluno').exists():
        return redirect('portal_vagas')
    # Fallback: home
    return redirect('home')


@login_required
def minhas_monitorias_cards(request):
    """
    View de atalho usada pelas templates para voltar ao espaço do monitor.
    Redireciona para o dashboard apropriado do monitor/professor ou para o
    portal de vagas quando o usuário não for monitor/professor.
    """
    user = request.user
    if user.groups.filter(name='Monitor').exists():
        return redirect('dashboard_monitor')
    if user.groups.filter(name='Professor').exists():
        return redirect('dashboard_professor')
    # Fallback: enviar ao portal de vagas (página pública/aluno)
    return redirect('portal_vagas')


@login_required
def participar_monitoria(request, turma_id):
    """
    Handler simples para links de 'participar' usados em templates.
    Atualmente redireciona para a página de detalhe da turma se existir,
    senão envia para a listagem de monitorias.
    """
    try:
        return redirect('detalhe_turma', turma_id=turma_id)
    except Exception:
        return redirect('listar_monitorias')


@login_required
def minhas_inscricoes(request):
    """
    Rota de compatibilidade para 'minhas_inscricoes' usada em templates.
    Atualmente redireciona para o portal de vagas; pode ser expandida para
    listar as inscrições do usuário quando necessário.
    """
    return redirect('portal_vagas')

@login_required
def listar_monitorias(request):
    """
    Lista monitorias (página pública/gestão conforme permissões).
    Renderiza templates/monitorias/listar.html
    """
    service = MonitoriaService()
    curso_filtro = request.GET.get('curso')
    status_filtro = request.GET.get('status')
    busca = request.GET.get('busca', '').strip()

    # tenta usar a API do service de forma robusta
    try:
        monitorias = service.listar_monitorias(curso_id=curso_filtro, status=status_filtro, busca=busca)
    except Exception:
        try:
            monitorias = service.listar(curso_id=curso_filtro, status=status_filtro, busca=busca)
        except Exception:
            monitorias = []

    context = {
        'monitorias': monitorias,
        'cursos': Curso.objects.filter(ativo=True),
        'filtros': {'curso': curso_filtro, 'status': status_filtro, 'busca': busca},
    }
    return render(request, 'monitorias/listar.html', context)



@login_required
def listar_monitorias(request):
    """
    Lista monitorias e renderiza templates/monitorias/listar.html
    """
    service = MonitoriaService()
    curso_filtro = request.GET.get('curso')
    status_filtro = request.GET.get('status')
    busca = request.GET.get('busca', '').strip()

    try:
        # tenta método mais específico do service
        monitorias = service.listar_monitorias(curso_id=curso_filtro, status=status_filtro, busca=busca)
    except AttributeError:
        # fallback para métodos com outro nome
        try:
            monitorias = service.listar(curso_id=curso_filtro, status=status_filtro, busca=busca)
        except Exception:
            monitorias = []
    except Exception:
        monitorias = []

    context = {
        'monitorias': monitorias,
        'cursos': Curso.objects.filter(ativo=True),
        'filtros': {'curso': curso_filtro, 'status': status_filtro, 'busca': busca},
    }
    return render(request, 'monitorias/listar.html', context)


def listar_presencas(request):
    """
    Lista presenças com filtros simples (turma, aluno, data, status).
    Usa PresencaService quando disponível, senão faz fallback direto no model.
    """
    service = PresencaService()
    turma_id = request.GET.get('turma')
    aluno_id = request.GET.get('aluno')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    status = request.GET.get('status')

    try:
        presencas = service.listar_presencas(
            turma_id=turma_id or None,
            aluno_id=aluno_id or None,
            data_inicio=data_inicio or None,
            data_fim=data_fim or None,
            status=status or None
        )
    except AttributeError:
        # fallback direto no model caso o service não implemente o método
        qs = Presenca.objects.all().select_related('aluno', 'turma')
        if turma_id:
            qs = qs.filter(turma_id=turma_id)
        if aluno_id:
            qs = qs.filter(aluno_id=aluno_id)
        if status:
            qs = qs.filter(status=status)
        if data_inicio:
            qs = qs.filter(data__gte=data_inicio)
        if data_fim:
            qs = qs.filter(data__lte=data_fim)
        presencas = qs.order_by('-data')

    context = {
        'presencas': presencas,
        'turmas': Turma.objects.filter(ativo=True),
    }
    return render(request, 'presencas/listar.html', context)


@login_required
def perfil(request):
    """
    Exibe o perfil do usuário logado.
    Usa PerfilService quando disponível para montar o contexto.
    """
    service = PerfilService()
    # Preferir API do service que monta o contexto completo
    if hasattr(service, 'get_perfil_context'):
        try:
            context = service.get_perfil_context(request.user) or {}
        except Exception:
            context = {}
    else:
        # Tenta compatibilidade com implementações antigas
        context = {}
        try:
            if hasattr(service, 'get_perfil_por_email'):
                perfil_obj = service.get_perfil_por_email(request.user.email)
                # Se o service retornar um dict já com chaves, usa-o
                if isinstance(perfil_obj, dict):
                    context.update(perfil_obj)
                else:
                    context['perfil'] = perfil_obj
        except Exception:
            # fallback básico
            context['perfil'] = {
                'nome': getattr(request.user, 'get_full_name', lambda: str(request.user))(),
                'email': getattr(request.user, 'email', ''),
            }

    # Garantir chaves mínimas esperadas pelos templates
    if 'usuario' not in context:
        context['usuario'] = request.user
    if 'aluno' not in context:
        context.setdefault('aluno', None)
    if 'professor' not in context:
        context.setdefault('professor', None)
    # Flag conveniente para templates
    context['is_professor'] = request.user.groups.filter(name='Professor').exists()

    return render(request, 'perfil.html', context)

@login_required
def atualizar_perfil_rapido(request):
    """
    Atualiza campos básicos do perfil do usuário.
    - Se PerfilService implementar update_perfil_por_email, usa-o.
    - Fallback: atualiza User (first_name, last_name, email) diretamente.
    Aceita também upload simples em 'avatar' (passa para o service se suportado).
    Retorna JSON quando requisitado via AJAX, caso contrário redireciona para 'perfil'.
    """
    service = PerfilService()
    data = {
        'nome': request.POST.get('nome', '').strip(),
        'email': request.POST.get('email', '').strip(),
        'telefone': request.POST.get('telefone', '').strip(),
        'curso_id': request.POST.get('curso') or None,
    }
    avatar = request.FILES.get('avatar')

    try:
        # tenta usar API do service
        if hasattr(service, 'update_perfil_por_email'):
            service.update_perfil_por_email(request.user.email, data, avatar=avatar)
        elif hasattr(service, 'atualizar_perfil'):
            service.atualizar_perfil(request.user.email, data, avatar=avatar)
        else:
            # fallback direto no User model
            User = get_user_model()
            try:
                user = User.objects.get(email=request.user.email)
            except User.DoesNotExist:
                user = request.user
            # divide nome em first/last se possível
            nome = data.get('nome') or ''
            parts = nome.split(None, 1)
            user.first_name = parts[0] if parts else ''
            user.last_name = parts[1] if len(parts) > 1 else ''
            if data.get('email'):
                user.email = data['email']
            user.save()
            # se houver service que possa associar avatar, tenta chamar
            if avatar and hasattr(service, 'salvar_avatar_por_email'):
                try:
                    service.salvar_avatar_por_email(request.user.email, avatar)
                except Exception:
                    pass
    except Exception as e:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)
        messages.error(request, f'Erro ao atualizar perfil: {str(e)}')
        return redirect('perfil')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'ok': True})
    messages.success(request, 'Perfil atualizado com sucesso.')
    return redirect('perfil')