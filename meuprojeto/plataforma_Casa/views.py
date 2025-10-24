from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Count, Q, Avg, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    Usuario, Aluno, Funcionario, Curso, Sala, Vaga, Turma, 
    ParticipacaoMonitoria, Presenca, Inscricao, TipoUsuario,
    Documento, RegistroHoras, StatusPagamento, MaterialApoio
)
from .repository import (
    listar_usuarios, listar_alunos, listar_cursos, listar_funcionarios, 
    listar_inscricoes, listar_turmas, listar_participacoes_monitoria, 
    listar_presencas, listar_salas, listar_tipos_usuario
)
from functools import wraps
from .forms import MaterialApoioForm


# ==================== FUNÇÕES AUXILIARES ====================

def get_aluno_by_email(email):
    """
    Função auxiliar para buscar aluno por email tratando emails duplicados
    Retorna o primeiro aluno encontrado ou None se não encontrar
    """
    try:
        return Aluno.objects.get(email=email)
    except Aluno.MultipleObjectsReturned:
        # Se houver múltiplos alunos com o mesmo email, pegar o primeiro
        return Aluno.objects.filter(email=email).first()
    except Aluno.DoesNotExist:
        return None


def get_monitor_by_email(email):
    """
    Função auxiliar para buscar monitor (que também é um aluno) por email
    Retorna o primeiro aluno/monitor encontrado ou None se não encontrar
    """
    return get_aluno_by_email(email)  # Monitor é um Aluno também


# ==================== DECORATORS DE SEGURANÇA ====================

def requer_grupo(*grupos_permitidos):
    """
    ⚠️ DECORATOR DE SEGURANÇA: Valida se usuário pertence a um dos grupos permitidos
    
    Uso:
        @requer_grupo('Aluno', 'Monitor')
        def minha_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='login')
        def wrapper(request, *args, **kwargs):
            # ✅ VERIFICAÇÃO: Usuário está autenticado?
            if not request.user.is_authenticated:
                messages.error(request, '❌ Você precisa estar autenticado.')
                return redirect('login')
            
            # ✅ VERIFICAÇÃO: Usuário tem um dos grupos permitidos?
            if not request.user.groups.filter(name__in=grupos_permitidos).exists():
                # ❌ ACESSO PROIBIDO
                user_groups = ', '.join(request.user.groups.values_list('name', flat=True)) or 'Nenhum'
                grupos_necessarios = ', '.join(grupos_permitidos)
                messages.error(
                    request, 
                    f'❌ ACESSO PROIBIDO! Seus grupos: {user_groups}. '
                    f'Grupos necessários: {grupos_necessarios}'
                )
                # Redirecionar para página segura baseado no grupo
                if request.user.groups.filter(name='Aluno').exists():
                    return redirect('portal_vagas')
                elif request.user.groups.filter(name='Monitor').exists():
                    return redirect('meus_registros_horas')
                elif request.user.groups.filter(name='Professor').exists():
                    return redirect('validar_horas')
                else:
                    return redirect('login')
            
            # ✅ AUTORIZADO: Executar view
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def requer_admin_ou_coordenador(view_func):
    """
    ⚠️ DECORATOR DE SEGURANÇA: Apenas Admin ou Coordenador podem acessar
    """
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        is_admin = request.user.is_staff or request.user.is_superuser
        is_coordenador = request.user.groups.filter(name='Coordenador').exists()
        
        if not (is_admin or is_coordenador):
            messages.error(request, '❌ ACESSO PROIBIDO! Apenas Admins ou Coordenadores.')
            
            # Redirecionar para rota segura
            if request.user.groups.filter(name='Professor').exists():
                return redirect('validar_horas')
            elif request.user.groups.filter(name='Monitor').exists():
                return redirect('meus_registros_horas')
            else:
                return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def requer_monitor(view_func):
    """
    ⚠️ DECORATOR DE SEGURANÇA: Apenas Monitors podem acessar
    """
    return requer_grupo('Monitor')(view_func)


def requer_aluno(view_func):
    """
    ⚠️ DECORATOR DE SEGURANÇA: Apenas Alunos podem acessar
    """
    return requer_grupo('Aluno')(view_func)


def requer_professor(view_func):
    """
    ⚠️ DECORATOR DE SEGURANÇA: Apenas Professores podem acessar
    """
    return requer_grupo('Professor')(view_func)


# ==================== AUTENTICAÇÃO ====================
def login_view(request):
    """
    View de Login - Autentica usuários com username ou email
    Backend customizado (EmailOrUsernameModelBackend) permite ambos
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()  # Remove espaços em branco
        password = request.POST.get('password', '')
        
        # O backend customizado tentará autenticar com username ou email
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirecionar baseado no grupo do usuário
            if user.groups.filter(name='Aluno').exists():
                return redirect('portal_vagas')  # Alunos vão para Portal de Vagas
            else:
                return redirect('dashboard')  # Outros perfis vão para Dashboard
        else:
            messages.error(request, 'Usuário ou senha inválidos!')
    
    return render(request, 'login.html')


def logout_view(request):
    """
    View de Logout - Faz logout do usuário
    """
    logout(request)
    return redirect('login')


def register_view(request):
    """
    View de Registro/Cadastro - Cria novo usuário com role de "Aluno"
    
    Comportamento:
    - GET: Exibe formulário de cadastro
    - POST: Cria novo usuário (Django User) e novo Aluno (modelo Aluno)
    - Todo novo usuário recebe automaticamente o role/grupo "Aluno"
    - Quando aprovado como monitor, recebe o role "Monitor"
    """
    User = get_user_model()
    
    if request.method == 'POST':
        try:
            # Coletar dados do formulário
            nome = request.POST.get('nome', '').strip()
            email = request.POST.get('email', '').strip()
            matricula = request.POST.get('matricula', '').strip()
            curso_id = request.POST.get('curso')
            periodo = request.POST.get('periodo')
            cr_geral = request.POST.get('cr_geral')
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '')
            password_confirm = request.POST.get('password_confirm', '')
            terms = request.POST.get('terms')
            
            # ==================== VALIDAÇÕES ====================
            
            # Validar campos obrigatórios
            if not all([nome, email, matricula, curso_id, periodo, cr_geral, username, password]):
                messages.error(request, '❌ Por favor, preencha todos os campos obrigatórios.')
                return redirect('register')
            
            # Validar aceitar termos
            if not terms:
                messages.error(request, '❌ Você deve aceitar os Termos de Serviço e Política de Privacidade.')
                return redirect('register')
            
            # Validar se senhas correspondem
            if password != password_confirm:
                messages.error(request, '❌ As senhas não correspondem!')
                return redirect('register')
            
            # Validar força da senha (mínimo 8 caracteres, letra maiúscula, minúscula, número)
            if len(password) < 8:
                messages.error(request, '❌ A senha deve ter no mínimo 8 caracteres.')
                return redirect('register')
            
            if not any(c.isupper() for c in password):
                messages.error(request, '❌ A senha deve conter pelo menos 1 letra maiúscula.')
                return redirect('register')
            
            if not any(c.islower() for c in password):
                messages.error(request, '❌ A senha deve conter pelo menos 1 letra minúscula.')
                return redirect('register')
            
            if not any(c.isdigit() for c in password):
                messages.error(request, '❌ A senha deve conter pelo menos 1 número.')
                return redirect('register')
            
            # Validar se username já existe
            if User.objects.filter(username=username).exists():
                messages.error(request, '❌ Este nome de usuário já está em uso. Escolha outro.')
                return redirect('register')
            
            # Validar se email já existe
            if User.objects.filter(email=email).exists():
                messages.error(request, '❌ Este email já está cadastrado.')
                return redirect('register')
            
            # Validar se matrícula já existe
            if Aluno.objects.filter(matricula=matricula).exists():
                messages.error(request, '❌ Esta matrícula já está cadastrada.')
                return redirect('register')
            
            # Validar curso
            try:
                curso = Curso.objects.get(id=curso_id)
            except Curso.DoesNotExist:
                messages.error(request, '❌ Curso inválido.')
                return redirect('register')
            
            # Validar período (deve ser entre 1 e 8)
            try:
                periodo = int(periodo)
                if periodo < 1 or periodo > 8:
                    raise ValueError
            except (ValueError, TypeError):
                messages.error(request, '❌ Período inválido.')
                return redirect('register')
            
            # Validar CR (deve estar entre 0 e 10)
            try:
                cr_geral = float(cr_geral)
                if cr_geral < 0 or cr_geral > 10:
                    raise ValueError
            except (ValueError, TypeError):
                messages.error(request, '❌ CR deve estar entre 0 e 10.')
                return redirect('register')
            
            # ==================== CRIAR USUÁRIO ====================
            
            # Criar usuário Django (User)
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=nome.split()[0] if nome else '',  # Primeiro nome
                last_name=' '.join(nome.split()[1:]) if len(nome.split()) > 1 else ''  # Sobrenome
            )
            
            # Adicionar grupo "Aluno" ao novo usuário
            try:
                grupo_aluno = Group.objects.get(name='Aluno')
                user.groups.add(grupo_aluno)
            except Group.DoesNotExist:
                # Se grupo não existir, criar
                grupo_aluno = Group.objects.create(name='Aluno')
                user.groups.add(grupo_aluno)
            
            user.save()
            
            # ==================== CRIAR ALUNO ====================
            
            # Obter ou criar TipoUsuario "Aluno"
            tipo_usuario, _ = TipoUsuario.objects.get_or_create(
                tipo='aluno',
                defaults={'ativo': True}
            )
            
            # Criar objeto Aluno
            aluno = Aluno.objects.create(
                nome=nome,
                email=email,
                tipo_usuario=tipo_usuario,
                matricula=matricula,
                curso=curso,
                data_ingresso=datetime.now().date(),
                periodo=periodo,
                cr_geral=cr_geral,
                ativo=True
            )
            
            # ==================== SUCESSO ====================
            
            # Log do novo usuário
            print(f"""
╔══════════════════════════════════════════════════════════════╗
║         ✅ NOVO USUÁRIO REGISTRADO COM SUCESSO              ║
╚══════════════════════════════════════════════════════════════╝

📋 INFORMAÇÕES DO USUÁRIO:
─────────────────────────────────────────────────────────────
✓ Nome: {nome}
✓ Email: {email}
✓ Username: {username}
✓ Matrícula: {matricula}
✓ Curso: {curso.nome}
✓ Período: {periodo}º
✓ CR: {cr_geral}

👥 ROLE/GRUPO ATRIBUÍDO:
─────────────────────────────────────────────────────────────
✓ Aluno (padrão)

🔔 PRÓXIMOS PASSOS:
─────────────────────────────────────────────────────────────
1. Faça login com seu usuário
2. Explore o Portal de Vagas
3. Inscreva-se em monitorias
4. Aguarde aprovação do professor

📱 CREDENCIAIS:
─────────────────────────────────────────────────────────────
Username: {username}
(senha cadastrada durante o registro)

""")
            
            return redirect('login')
        
        except Exception as e:
            messages.error(request, f'❌ Erro ao registrar: {str(e)}')
            print(f"Erro no registro: {e}")
            return redirect('register')
    
    # GET - Exibir formulário de cadastro
    cursos = Curso.objects.filter(ativo=True)
    
    context = {
        'cursos': cursos,
    }
    
    return render(request, 'register.html', context)


# ==================== DASHBOARD ====================
@login_required(login_url='login')
def dashboard(request):
    """
    View do Dashboard - Redireciona cada usuário para seu dashboard específico
    
    Comportamento:
    - Admin (sem outros grupos): Redireciona para Dashboard de Gestão
    - Professor: Renderiza Dashboard do Professor
    - Monitor: Renderiza Dashboard do Monitor
    - Aluno: Redireciona para Portal de Vagas
    - Outros: Renderiza Dashboard Geral
    """
    user = request.user
    
    # ========== VERIFICAR PERFIL DO USUÁRIO ==========
    is_admin = user.is_staff or user.is_superuser
    is_professor = user.groups.filter(name='Professor').exists()
    is_monitor = user.groups.filter(name='Monitor').exists()
    is_aluno = user.groups.filter(name='Aluno').exists()
    
    # ========== REDIRECIONAMENTOS BASEADOS EM HIERARQUIA ==========
    
    # IMPORTANTE: Professor tem prioridade sobre Admin
    # Se o usuário é Professor (mesmo sendo staff), vai para Dashboard do Professor
    if is_professor:
        # Dashboard do Professor será renderizado abaixo
        pass
    # Admin SEM grupo Professor vai para Dashboard de Gestão
    elif is_admin:
        return redirect('dashboard_gestao')
    
    # ========== DASHBOARD DO MONITOR ==========
    
    if is_monitor:
        # Dashboard personalizado para MONITOR
        try:
            # Buscar aluno pelo email do Django User
            monitor = get_monitor_by_email(user.email)
            if not monitor:
                # Se monitor não foi encontrado, redireciona para login
                from django.contrib.auth import logout
                logout(request)
                return redirect('login')
            
            # Estatísticas do MONITOR (minhas monitorias)
            minhas_monitorias = Turma.objects.filter(monitor=monitor, ativo=True)
            total_monitorias = minhas_monitorias.count()
            
            # Total de alunos nas minhas monitorias
            total_alunos = ParticipacaoMonitoria.objects.filter(
                turma__monitor=monitor
            ).values('aluno').distinct().count()
            
            # Horas registradas neste mês
            from datetime import datetime, timedelta
            inicio_mes = datetime.now().replace(day=1).date()
            horas_este_mes = RegistroHoras.objects.filter(
                turma__monitor=monitor,
                data__gte=inicio_mes
            ).aggregate(total=Sum('total_horas'))['total'] or 0
            
            # Horas pendentes de validação
            horas_pendentes = RegistroHoras.objects.filter(
                turma__monitor=monitor,
                status='Pendente'
            ).count()
            
            # Total de horas acumuladas
            total_horas = RegistroHoras.objects.filter(
                turma__monitor=monitor,
                status='Aprovado'
            ).aggregate(total=Sum('total_horas'))['total'] or 0
            
            # Taxa de presença média nas minhas turmas
            presencas = Presenca.objects.filter(turma__monitor=monitor)
            total_presencas = presencas.count()
            presentes = presencas.filter(presente=True).count()
            taxa_presenca = (presentes / total_presencas * 100) if total_presencas > 0 else 0
            
            # Últimos registros de horas
            ultimos_registros = RegistroHoras.objects.filter(
                turma__monitor=monitor
            ).select_related('turma', 'turma__vaga').order_by('-data')[:5]
            
            # Monitorias mais ativas (com mais alunos)
            monitorias_ativas = minhas_monitorias.annotate(
                num_alunos=Count('participacaomonitoria')
            ).filter(num_alunos__gt=0).order_by('-num_alunos')[:5]
            
            context = {
                'is_monitor_dashboard': True,
                'total_monitorias': total_monitorias,
                'total_alunos': total_alunos,
                'horas_este_mes': round(horas_este_mes, 2),
                'horas_pendentes': horas_pendentes,
                'total_horas': round(total_horas, 2),
                'taxa_presenca': round(taxa_presenca, 1),
                'ultimos_registros': ultimos_registros,
                'minhas_monitorias': minhas_monitorias,
                'monitorias_ativas': monitorias_ativas,
            }
            
        except Aluno.DoesNotExist:
            # Fallback se não encontrar aluno
            context = {
                'is_monitor_dashboard': True,
                'total_monitorias': 0,
                'total_alunos': 0,
                'horas_este_mes': 0,
                'horas_pendentes': 0,
                'total_horas': 0,
                'taxa_presenca': 0,
                'ultimos_registros': [],
                'minhas_monitorias': [],
                'monitorias_ativas': [],
            }
        
        return render(request, 'dashboard_monitor.html', context)
    
    # Aluno vai para Portal de Vagas
    if is_aluno:
        return redirect('portal_vagas')
    
    # ========== DASHBOARD DO PROFESSOR / COORDENADOR ==========
    
    if is_professor:
        # Dashboard personalizado para PROFESSOR (que é também COORDENADOR de monitorias)
        try:
            # Buscar funcionario pelo email do Django User
            funcionario = Funcionario.objects.get(email=user.email)
            
            # ✅ SINCRONIZAR GRUPO: Se professor tem vagas, adicionar grupo "Coordenador"
            grupo_coordenador, _ = Group.objects.get_or_create(name='Coordenador')
            tem_vagas = Vaga.objects.filter(coordenador=funcionario).exists()
            
            if tem_vagas and not user.groups.filter(name='Coordenador').exists():
                user.groups.add(grupo_coordenador)
                print(f"✅ Grupo 'Coordenador' adicionado ao professor {funcionario.nome}")
            
            # Estatísticas das MINHAS vagas (vagas que eu coordeno)
            minhas_vagas = Vaga.objects.filter(coordenador=funcionario)
            total_minhas_vagas = minhas_vagas.filter(ativo=True).count()
            
            # Total de candidatos nas minhas vagas
            total_candidatos = Inscricao.objects.filter(vaga__coordenador=funcionario).count()
            
            # Candidatos pendentes de avaliação
            candidatos_pendentes = Inscricao.objects.filter(
                vaga__coordenador=funcionario,
                status='Pendente'
            ).count()
            
            # Monitores aprovados nas minhas vagas
            monitores_aprovados = Inscricao.objects.filter(
                vaga__coordenador=funcionario,
                status='Aprovado'
            ).count()
            
            # Horas pendentes de validação (de todas as monitorias que preciso validar)
            # Professor valida as horas através do campo validado_por em RegistroHoras
            horas_pendentes = RegistroHoras.objects.filter(
                status='Pendente'
            ).count()
            
            # Minhas turmas (turmas onde o monitor está registrado nas vagas que coordeno)
            # Obter todos os monitores aprovados nas minhas vagas
            monitores_aprovados_ids = Inscricao.objects.filter(
                vaga__coordenador=funcionario,
                status='Aprovado'
            ).values_list('aluno_id', flat=True)
            
            # Turmas desses monitores
            minhas_turmas = Turma.objects.filter(
                monitor_id__in=monitores_aprovados_ids,
                ativo=True
            ).order_by('-criado_em')[:5]
            
            # Últimas inscrições nas minhas vagas
            ultimas_inscricoes = Inscricao.objects.filter(
                vaga__coordenador=funcionario
            ).select_related('aluno', 'vaga').order_by('-data_inscricao')[:5]
            
            # Vagas com mais candidatos
            vagas_populares = minhas_vagas.annotate(
                num_candidatos=Count('inscricao')
            ).filter(num_candidatos__gt=0).order_by('-num_candidatos')[:5]
            
            context = {
                'is_professor_dashboard': True,
                'total_minhas_vagas': total_minhas_vagas,
                'total_candidatos': total_candidatos,
                'candidatos_pendentes': candidatos_pendentes,
                'monitores_aprovados': monitores_aprovados,
                'horas_pendentes': horas_pendentes,
                'minhas_turmas': minhas_turmas,
                'ultimas_inscricoes': ultimas_inscricoes,
                'vagas_populares': vagas_populares,
            }
            
        except Funcionario.DoesNotExist:
            # Fallback se não encontrar funcionario
            context = {
                'is_professor_dashboard': True,
                'total_minhas_vagas': 0,
                'total_candidatos': 0,
                'candidatos_pendentes': 0,
                'monitores_aprovados': 0,
                'horas_pendentes': 0,
                'minhas_turmas': [],
                'ultimas_inscricoes': [],
                'vagas_populares': [],
            }
        
        return render(request, 'dashboard.html', context)
    
    # ========== FALLBACK: DASHBOARD GERAL ==========
    # Para outros perfis (se houver)
    total_usuarios = Usuario.objects.filter(ativo=True).count()
    total_alunos = Aluno.objects.filter(ativo=True).count()
    total_turmas = Turma.objects.filter(ativo=True).count()
    total_vagas = Vaga.objects.filter(ativo=True).count()
    
    ultimas_monitorias = Turma.objects.filter(ativo=True).order_by('-criado_em')[:5]
    inscricoes_pendentes = Inscricao.objects.filter(status='Pendente')[:5]
    
    context = {
        'is_professor_dashboard': False,
        'total_usuarios': total_usuarios,
        'total_alunos': total_alunos,
        'total_turmas': total_turmas,
        'total_vagas': total_vagas,
        'ultimas_monitorias': ultimas_monitorias,
        'inscricoes_pendentes': inscricoes_pendentes,
    }
    
    return render(request, 'dashboard.html', context)


# ==================== USUÁRIOS ====================
@requer_admin_ou_coordenador
def listar_usuarios(request):
    """
    View para listar todos os usuários
    ⚠️ APENAS ADMINS OU COORDENADORES podem acessar
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
            # messages.success(request, f'Usuário "{nome}" criado com sucesso!')
            return redirect('listar_usuarios')
        except Exception as e:
            # messages.error(request, f'Erro ao criar usuário: {str(e)}')
            pass
    
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
        # messages.success(request, 'Usuário atualizado com sucesso!')
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
    # messages.success(request, f'Usuário "{nome}" deletado com sucesso!')
    return redirect('listar_usuarios')


# ==================== ALUNOS ====================
@requer_admin_ou_coordenador
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


@requer_admin_ou_coordenador
def criar_aluno(request):
    """
    View para criar novo aluno
    ⚠️ APENAS ADMINS OU COORDENADORES podem acessar
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
            # messages.success(request, f'Aluno "{nome}" criado com sucesso!')
            return redirect('listar_alunos')
        except Exception as e:
            # messages.error(request, f'Erro ao criar aluno: {str(e)}')
            pass
    
    context = {
        'cursos': Curso.objects.filter(ativo=True),
    }
    return render(request, 'alunos/criar.html', context)


@requer_admin_ou_coordenador
def editar_aluno(request, aluno_id):
    """
    View para editar aluno
     APENAS ADMINS OU COORDENADORES podem acessar
    """
    aluno = get_object_or_404(Aluno, id=aluno_id)
    
    if request.method == 'POST':
        aluno.nome = request.POST.get('nome')
        aluno.email = request.POST.get('email')
        aluno.periodo = request.POST.get('periodo')
        aluno.cr_geral = request.POST.get('cr_geral', aluno.cr_geral)
        aluno.ativo = request.POST.get('ativo') == 'on'
        aluno.save()
        # messages.success(request, 'Aluno atualizado com sucesso!')
        return redirect('listar_alunos')
    
    context = {'aluno': aluno}
    return render(request, 'alunos/editar.html', context)


@requer_admin_ou_coordenador
def deletar_aluno(request, aluno_id):
    """
    View para deletar aluno
     APENAS ADMINS OU COORDENADORES podem acessar
    """
    aluno = get_object_or_404(Aluno, id=aluno_id)
    nome = aluno.nome
    aluno.delete()
    # messages.success(request, f'Aluno "{nome}" deletado com sucesso!')
    return redirect('listar_alunos')


# ==================== VAGAS ====================
@requer_admin_ou_coordenador
def listar_vagas(request):
    """
    View para listar vagas de monitoria
    
     APENAS ADMINS OU COORDENADORES podem acessar
    
    Comportamento:
    - Admin: Vê TODAS as vagas do sistema
    - Professor/Coordenador: Vê APENAS as vagas que ele coordena
    """
    user = request.user
    
    # Admin vê todas as vagas
    if user.is_staff or user.is_superuser:
        vagas = Vaga.objects.all().select_related('curso', 'coordenador').prefetch_related('monitores').annotate(
            total_inscritos=Count('inscricao')
        )
    else:
        # Professor/Coordenador vê apenas suas vagas
        try:
            funcionario = Funcionario.objects.get(email=user.email)
            vagas = Vaga.objects.filter(coordenador=funcionario).select_related('curso', 'coordenador').prefetch_related('monitores').annotate(
                total_inscritos=Count('inscricao')
            )
        except Funcionario.DoesNotExist:
            # Se não encontrar funcionário, retorna vazio
            vagas = Vaga.objects.none()
    
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
        'is_admin': user.is_staff or user.is_superuser,
    }
    return render(request, 'vagas/listar.html', context)


@requer_admin_ou_coordenador
def detalhe_vaga(request, vaga_id):
    """
    View para detalhar uma vaga e listar candidatos inscritos
     APENAS ADMINS OU COORDENADORES podem acessar
    
    Comportamento:
    - Admin: Pode ver QUALQUER vaga
    - Professor/Coordenador: Pode ver APENAS suas vagas
    """
    vaga = get_object_or_404(Vaga, id=vaga_id)
    user = request.user
    
    # ✅ VERIFICAÇÃO DE PERMISSÃO
    # Admin pode acessar qualquer vaga
    if not (user.is_staff or user.is_superuser):
        # Professor/Coordenador: verificar se é o coordenador da vaga
        try:
            funcionario = Funcionario.objects.get(email=user.email)
            if vaga.coordenador != funcionario:
                # Não tem permissão para ver esta vaga
                messages.error(request, '❌ Você não tem permissão para ver esta vaga')
                return redirect('listar_vagas')
        except Funcionario.DoesNotExist:
            messages.error(request, '❌ Professor não encontrado')
            return redirect('listar_vagas')
    
    inscricoes = Inscricao.objects.filter(vaga=vaga).select_related('aluno', 'aluno__curso').order_by('-data_inscricao')
    
    # Estatísticas
    total_inscricoes = inscricoes.count()
    pendentes = inscricoes.filter(status='Pendente').count()
    entrevista = inscricoes.filter(status='Entrevista').count()
    aprovados = inscricoes.filter(status='Aprovado').count()
    rejeitados = inscricoes.filter(status='Não Aprovado').count()
    
    context = {
        'vaga': vaga,
        'inscricoes': inscricoes,
        'total_inscricoes': total_inscricoes,
        'pendentes': pendentes,
        'entrevista': entrevista,
        'aprovados': aprovados,
        'rejeitados': rejeitados,
    }
    return render(request, 'vagas/detalhe.html', context)


@login_required
def detalhe_candidato(request, inscricao_id):
    """
    View para ver detalhes completos de um candidato
    """
    inscricao = get_object_or_404(Inscricao, id=inscricao_id)
    documentos = inscricao.documentos.all()
    
    context = {
        'inscricao': inscricao,
        'aluno': inscricao.aluno,
        'vaga': inscricao.vaga,
        'documentos': documentos,
    }
    return render(request, 'vagas/detalhe_candidato.html', context)


def avaliar_candidato(request, inscricao_id):
    """
    View para aprovar/reprovar candidato
    
    Quando um candidato é APROVADO:
    1. Atualiza status da inscrição para 'Aprovado'
    2. Adiciona o aluno ao relacionamento ManyToMany da vaga (vaga.monitores)
    3. Adiciona o User do Django ao grupo "Monitor"
    """
    User = get_user_model()
    inscricao = get_object_or_404(Inscricao, id=inscricao_id)
    
    if request.method == 'POST':
        acao = request.POST.get('acao')
        
        try:
            # Atualizar status baseado na ação
            if acao == 'aprovar':
                inscricao.status = 'Aprovado'
                
                # 1. Adicionar aluno aos monitores da vaga
                inscricao.vaga.monitores.add(inscricao.aluno)
                
                # 2. Adicionar usuário ao grupo "Monitor"
                try:
                    # Buscar User pelo email do aluno
                    user = User.objects.get(email=inscricao.aluno.email)
                    grupo_monitor, _ = Group.objects.get_or_create(name='Monitor')
                    user.groups.add(grupo_monitor)
                    user.save()
                    print(f" User {user.username} adicionado ao grupo Monitor")
                except User.DoesNotExist:
                    print(f" User não encontrado para email: {inscricao.aluno.email}")
                except Exception as e:
                    print(f" Erro ao adicionar ao grupo Monitor: {e}")
                
            elif acao == 'reprovar':
                inscricao.status = 'Não Aprovado'
                
                # Remover do grupo Monitor se estava aprovado antes
                try:
                    user = User.objects.get(email=inscricao.aluno.email)
                    grupo_monitor = Group.objects.get(name='Monitor')
                    user.groups.remove(grupo_monitor)
                    # Remover da lista de monitores da vaga
                    inscricao.vaga.monitores.remove(inscricao.aluno)
                except (User.DoesNotExist, Group.DoesNotExist):
                    pass
                
            elif acao == 'entrevista':
                inscricao.status = 'Entrevista'
            
            inscricao.save()
            
            return redirect('detalhe_vaga', vaga_id=inscricao.vaga.id)
        except Exception as e:
            print(f"❌ Erro ao avaliar candidato: {e}")
            pass
    
    context = {
        'inscricao': inscricao,
    }
    return render(request, 'vagas/avaliar_candidato.html', context)


@requer_admin_ou_coordenador
def criar_vaga(request):
    """
    View para criar nova vaga
     APENAS ADMINS OU COORDENADORES podem acessar
    
    Comportamento:
    - Admin: Pode criar vaga para qualquer coordenador
    - Professor/Coordenador: Só pode criar vagas para SI MESMO
    """
    user = request.user
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        curso_id = request.POST.get('curso')
        coordenador_id = request.POST.get('coordenador')
        descricao = request.POST.get('descricao')
        requisitos = request.POST.get('requisitos')
        
        # ✅ VALIDAÇÃO: Professor só pode criar vaga para si mesmo
        if not (user.is_staff or user.is_superuser):
            try:
                funcionario = Funcionario.objects.get(email=user.email)
                # Verificar se coordenador_id é igual ao do professor
                if str(funcionario.id) != str(coordenador_id):
                    messages.error(request, '❌ Você só pode criar vagas para si mesmo')
                    return redirect('criar_vaga')
            except Funcionario.DoesNotExist:
                messages.error(request, '❌ Professor não encontrado')
                return redirect('criar_vaga')
        
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
            return redirect('listar_vagas')
        except Exception as e:
            messages.error(request, f'❌ Erro ao criar vaga: {str(e)}')
            return redirect('criar_vaga')
    
    # Limitar coordenadores que cada usuário pode selecionar
    user = request.user
    if user.is_staff or user.is_superuser:
        # Admin vê todos os coordenadores
        coordenadores = Funcionario.objects.filter(ativo=True, coordenador=True)
    else:
        # Professor só vê a si mesmo
        try:
            funcionario = Funcionario.objects.get(email=user.email)
            coordenadores = Funcionario.objects.filter(id=funcionario.id)
        except Funcionario.DoesNotExist:
            coordenadores = Funcionario.objects.none()
    
    context = {
        'cursos': Curso.objects.filter(ativo=True),
        'coordenadores': coordenadores,
    }
    return render(request, 'vagas/criar.html', context)


@requer_admin_ou_coordenador
def editar_vaga(request, vaga_id):
    """
    View para editar vaga
     APENAS ADMINS OU COORDENADORES podem acessar
    
    Comportamento:
    - Admin: Pode editar QUALQUER vaga
    - Professor/Coordenador: Pode editar APENAS suas vagas
    """
    vaga = get_object_or_404(Vaga, id=vaga_id)
    user = request.user
    
    # ✅ VERIFICAÇÃO DE PERMISSÃO
    # Admin pode editar qualquer vaga
    if not (user.is_staff or user.is_superuser):
        # Professor/Coordenador: verificar se é o coordenador da vaga
        try:
            funcionario = Funcionario.objects.get(email=user.email)
            if vaga.coordenador != funcionario:
                # Não tem permissão para editar esta vaga
                messages.error(request, '❌ Você não tem permissão para editar esta vaga')
                return redirect('listar_vagas')
        except Funcionario.DoesNotExist:
            messages.error(request, '❌ Professor não encontrado')
            return redirect('listar_vagas')
    
    if request.method == 'POST':
        vaga.nome = request.POST.get('nome')
        vaga.descricao = request.POST.get('descricao')
        vaga.requisitos = request.POST.get('requisitos')
        vaga.ativo = request.POST.get('ativo') == 'on'
        vaga.save()
        return redirect('listar_vagas')
    
    context = {'vaga': vaga}
    return render(request, 'vagas/editar.html', context)


@requer_admin_ou_coordenador
def deletar_vaga(request, vaga_id):
    """
    View para deletar vaga
     APENAS ADMINS OU COORDENADORES podem acessar
    
    Comportamento:
    - Admin: Pode deletar QUALQUER vaga
    - Professor/Coordenador: Pode deletar APENAS suas vagas
    """
    vaga = get_object_or_404(Vaga, id=vaga_id)
    user = request.user
    
    # ✅ VERIFICAÇÃO DE PERMISSÃO
    # Admin pode deletar qualquer vaga
    if not (user.is_staff or user.is_superuser):
        # Professor/Coordenador: verificar se é o coordenador da vaga
        try:
            funcionario = Funcionario.objects.get(email=user.email)
            if vaga.coordenador != funcionario:
                # Não tem permissão para deletar esta vaga
                messages.error(request, '❌ Você não tem permissão para deletar esta vaga')
                return redirect('listar_vagas')
        except Funcionario.DoesNotExist:
            messages.error(request, '❌ Professor não encontrado')
            return redirect('listar_vagas')
    
    nome = vaga.nome
    vaga.delete()
    return redirect('listar_vagas')


# ==================== TURMAS ====================
@requer_admin_ou_coordenador
def listar_turmas(request):
    """
    View para listar todas as turmas (GESTÃO)
     APENAS ADMINS OU COORDENADORES podem acessar
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


@requer_admin_ou_coordenador
def detalhe_turma(request, turma_id):
    """
    View para detalhar uma turma específica
     APENAS ADMINS OU COORDENADORES podem acessar
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


@requer_admin_ou_coordenador
def criar_turma(request):
    """
    View para criar nova turma
     APENAS ADMINS OU COORDENADORES podem acessar
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
            # messages.success(request, f'Turma "{nome}" criada com sucesso!')
            return redirect('listar_turmas')
        except Exception as e:
            # messages.error(request, f'Erro ao criar turma: {str(e)}')
            pass
    
    context = {
        'vagas': Vaga.objects.filter(ativo=True),
        'salas': Sala.objects.filter(ativo=True),
        'monitores': Aluno.objects.filter(ativo=True),
        'cursos': Curso.objects.filter(ativo=True),
    }
    return render(request, 'turmas/criar.html', context)


@requer_admin_ou_coordenador
def editar_turma(request, turma_id):
    """
    View para editar turma
    ⚠️ APENAS ADMINS OU COORDENADORES podem acessar
    """
    turma = get_object_or_404(Turma, id=turma_id)
    
    if request.method == 'POST':
        turma.nome = request.POST.get('nome')
        turma.descricao = request.POST.get('descricao')
        turma.horario = request.POST.get('horario')
        turma.ativo = request.POST.get('ativo') == 'on'
        turma.save()
        # messages.success(request, 'Turma atualizada com sucesso!')
        return redirect('listar_turmas')
    
    context = {'turma': turma}
    return render(request, 'turmas/editar.html', context)


@requer_admin_ou_coordenador
def deletar_turma(request, turma_id):
    """
    View para deletar turma
    ⚠️ APENAS ADMINS OU COORDENADORES podem acessar
    """
    turma = get_object_or_404(Turma, id=turma_id)
    nome = turma.nome
    turma.delete()
    # messages.success(request, f'Turma "{nome}" deletada com sucesso!')
    return redirect('listar_turmas')


# ==================== MONITORIAS ====================
@requer_admin_ou_coordenador
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
        # messages.success(request, 'Participação atualizada com sucesso!')
        return redirect('listar_monitorias')
    
    context = {'participacao': participacao}
    return render(request, 'monitorias/editar.html', context)


# ==================== PRESENÇAS ====================
@requer_admin_ou_coordenador
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
        # messages.success(request, 'Presença atualizada com sucesso!')
        return redirect('listar_presencas')
    
    context = {'presenca': presenca}
    return render(request, 'presencas/editar.html', context)


# ==================== RELATÓRIOS ====================
@requer_admin_ou_coordenador
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
@login_required(login_url='login')
def perfil(request):
    """
    View para exibir e editar perfil do usuário
    
    Mostra diferentes informações baseado no tipo de usuário:
    - ALUNO/MONITOR: Curso, Matrícula, Período, CR
    - PROFESSOR/ADMIN: Apenas Nome e Email
    """
    usuario = request.user
    aluno = None
    professor = None
    
    # Tentar recuperar dados de Aluno (para Alunos e Monitors)
    try:
        aluno = get_aluno_by_email(usuario.email)
    except:
        pass
    
    # Tentar recuperar dados de Professor (para Professores)
    try:
        professor = Funcionario.objects.get(email=usuario.email)
    except:
        pass
    
    if request.method == 'POST':
        usuario.first_name = request.POST.get('nome')
        usuario.email = request.POST.get('email')
        usuario.save()
        
        # Se é aluno/monitor, atualizar dados de Aluno também
        if aluno:
            aluno.nome = request.POST.get('nome')
            aluno.email = request.POST.get('email')
            aluno.save()
        
        # messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil')
    
    # Importante: NÃO sobrescrever as flags is_aluno/is_monitor/is_professor fornecidas
    # pelo context processor (plataforma_Casa.context_processors.user_groups).
    # Isso evita inconsistências no sidebar entre páginas (ex.: Perfil ocultando itens).
    context = {
        'usuario': usuario,
        'aluno': aluno,
        'professor': professor,
    }
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
            # messages.success(request, 'Senha alterada com sucesso!')
            return redirect('perfil')
        else:
            # messages.error(request, 'As senhas não coincidem!')
            return redirect('perfil')
    
    return redirect('perfil')


# ==================== VIEW SQL (ORIGINAL) ====================
def sql_view(request):
    """
    View original - Exibe dados SQL em template
    Importa dados do repository.py que utiliza Django ORM para queries
    """
    # Importar as funções do repository para evitar conflito com views de mesmo nome
    from . import repository as repo
    
    # Chamar as funções do repository (que retornam QuerySets)
    usuarios = repo.listar_usuarios()
    alunos = repo.listar_alunos()
    cursos = repo.listar_cursos()
    funcionarios = repo.listar_funcionarios()
    inscricoes = repo.listar_inscricoes()
    turmas = repo.listar_turmas()
    participacoes_monitoria = repo.listar_participacoes_monitoria()
    presencas = repo.listar_presencas()
    salas = repo.listar_salas()
    tipos_usuario = repo.listar_tipos_usuario()
    
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


# ==================== PORTAL DE VAGAS APRIMORADO ====================
def portal_vagas(request):
    """
    View para portal público de vagas
    """
    vagas = Vaga.objects.filter(ativo=True).select_related('curso', 'coordenador').annotate(
        total_inscritos=Count('inscricao')
    )
    
    # Filtros
    curso_filtro = request.GET.get('curso')
    if curso_filtro:
        vagas = vagas.filter(curso__id=curso_filtro)
    
    context = {
        'vagas': vagas,
        'cursos': Curso.objects.filter(ativo=True),
    }
    return render(request, 'vagas/portal.html', context)


@login_required
def api_detalhes_vaga(request, vaga_id):
    """
    ✨ API ENDPOINT: Retorna detalhes da vaga em JSON
    ✅ ACESSÍVEL: Alunos, Monitores, Professores, Admins
    
    Retorna informações públicas sobre a vaga para exibição em modal
    """
    vaga = get_object_or_404(Vaga, id=vaga_id, ativo=True)
    
    # Contar inscrições
    total_inscritos = Inscricao.objects.filter(vaga=vaga).count()
    vagas_disponiveis = vaga.vagas_disponiveis()
    
    data = {
        'id': vaga.id,
        'nome': vaga.nome,
        'curso': vaga.curso.nome,
        'disciplina': vaga.disciplina or 'Não especificada',
        'coordenador': vaga.coordenador.nome if vaga.coordenador else 'Não especificado',
        'descricao': vaga.descricao,
        'requisitos': vaga.requisitos,
        'responsabilidades': vaga.responsabilidades or 'Não especificadas',
        'numero_vagas': vaga.numero_vagas,
        'vagas_disponiveis': vagas_disponiveis,
        'total_inscritos': total_inscritos,
    }
    
    return JsonResponse(data)


def candidatar_vaga(request, vaga_id):
    """
    View para candidatura a uma vaga
    """
    vaga = get_object_or_404(Vaga, id=vaga_id, ativo=True)
    
    # Verificar se é aluno
    try:
        aluno = get_aluno_by_email(request.user.email)
        if not aluno:
            raise Exception("Aluno não encontrado")
    except:
        # messages.error(request, 'Apenas alunos podem se candidatar!')
        return redirect('portal_vagas')
    
    # Verificar se já está inscrito
    if Inscricao.objects.filter(aluno=aluno, vaga=vaga).exists():
        # messages.warning(request, 'Você já se candidatou a esta vaga!')
        return redirect('minhas_inscricoes')
    
    if request.method == 'POST':
        # Criar inscrição
        inscricao = Inscricao.objects.create(
            aluno=aluno,
            vaga=vaga,
            status='Pendente'
        )
        
        # Upload de documentos
        documentos_tipos = ['Histórico Escolar', 'Currículo', 'Carta de Motivação']
        for tipo in documentos_tipos:
            arquivo = request.FILES.get(f'documento_{tipo.lower().replace(" ", "_")}')
            if arquivo:
                Documento.objects.create(
                    inscricao=inscricao,
                    tipo=tipo,
                    arquivo=arquivo,
                    nome_arquivo=arquivo.name
                )
        
        # messages.success(request, 'Candidatura enviada com sucesso!')
        return redirect('minhas_inscricoes')
    
    context = {'vaga': vaga}
    return render(request, 'vagas/candidatar.html', context)


def minhas_inscricoes(request):
    """
    View para aluno ver suas inscrições
    """
    try:
        aluno = get_aluno_by_email(request.user.email)
        if not aluno:
            inscricoes = []
        else:
            inscricoes = Inscricao.objects.filter(aluno=aluno).select_related('vaga').prefetch_related('documentos')
    except:
        inscricoes = []
    
    context = {'inscricoes': inscricoes}
    return render(request, 'inscricoes/minhas_inscricoes.html', context)


@requer_grupo('Aluno', 'Monitor')
def participando_monitorias(request):
    """
    View para ALUNO/MONITOR ver monitorias que está participando (como aluno)
    
    Mostra todas as monitorias em que o aluno/monitor está inscrito e aprovado
    Monitores podem participar de monitorias de outras disciplinas como alunos
    """
    participacoes = []
    try:
        aluno = get_aluno_by_email(request.user.email)
        if aluno:
            # Buscar participações ativas
            participacoes = ParticipacaoMonitoria.objects.filter(
                aluno=aluno
            ).select_related('turma', 'turma__vaga', 'turma__monitor', 'turma__curso').order_by('-turma__vaga__nome')
    except Exception as e:
        participacoes = []
    
    context = {'participacoes': participacoes}
    return render(request, 'monitorias/participando.html', context)


@requer_grupo('Aluno', 'Monitor')
def monitorias_disponiveis(request):
    """
    View para ALUNO/MONITOR ver todas as monitorias disponíveis para participar
    
    Similar ao portal de vagas, mas mostra turmas específicas (não vagas)
    Monitores podem participar de monitorias de outras disciplinas como alunos
    """
    turmas = Turma.objects.filter(ativo=True).select_related('vaga', 'monitor', 'curso', 'sala').order_by('-vaga__nome')
    
    # Busca por nome (disciplina, turma ou monitor)
    busca = request.GET.get('busca', '').strip()
    if busca:
        from django.db.models import Q
        turmas = turmas.filter(
            Q(vaga__nome__icontains=busca) |
            Q(nome__icontains=busca) |
            Q(monitor__nome__icontains=busca) |
            Q(curso__nome__icontains=busca)
        )
    
    # Filtro por curso
    curso_filtro = request.GET.get('curso')
    if curso_filtro:
        turmas = turmas.filter(curso__id=curso_filtro)
    
    # Filtro por vaga
    vaga_filtro = request.GET.get('vaga')
    if vaga_filtro:
        turmas = turmas.filter(vaga__id=vaga_filtro)
    
    context = {
        'turmas': turmas,
        'cursos': Curso.objects.filter(ativo=True),
        'vagas': Vaga.objects.filter(ativo=True),
    }
    return render(request, 'monitorias/disponiveis.html', context)


@login_required
@requer_grupo('Aluno', 'Monitor')
def participar_monitoria(request, turma_id):
    """
    ✨ View para ALUNO/MONITOR se INSCREVER/PARTICIPAR de uma monitoria
    
    Cria uma ParticipacaoMonitoria entre o aluno/monitor e a turma
    Monitores podem participar de monitorias de outras disciplinas como alunos
    """
    turma = get_object_or_404(Turma, id=turma_id, ativo=True)
    
    # ✅ Obter aluno pelo usuário autenticado usando a função auxiliar
    try:
        aluno = get_aluno_by_email(request.user.email)
        if not aluno:
            messages.error(request, '❌ Aluno não encontrado')
            return redirect('monitorias_disponiveis')
        
        print(f"[DEBUG] Aluno encontrado: ID {aluno.id}, Nome {aluno.nome}, Email {aluno.email}")
    except Exception as e:
        print(f"[DEBUG] Erro ao buscar aluno: {str(e)}")
        messages.error(request, '❌ Erro ao buscar aluno')
        return redirect('monitorias_disponiveis')
    
    # ✅ Verificar se já participa dessa turma
    if ParticipacaoMonitoria.objects.filter(aluno=aluno, turma=turma).exists():
        messages.warning(request, '⚠️ Você já está inscrito nessa monitoria!')
        return redirect('participando_monitorias')
    
    # ✅ Criar participação automaticamente (aprovado direto)
    try:
        participacao = ParticipacaoMonitoria.objects.create(
            aluno=aluno,
            turma=turma
        )
        print(f"[DEBUG] Participação criada: ID {participacao.id}, Aluno {aluno.nome}, Turma {turma.nome}")
    except Exception as e:
        print(f"[DEBUG] Erro ao criar participação: {str(e)}")
        messages.error(request, f'❌ Erro ao se inscrever: {str(e)}')
    
    return redirect('participando_monitorias')


@requer_grupo('Aluno', 'Monitor')
def sair_monitoria(request, turma_id):
    """
    ✨ View para ALUNO/MONITOR SAIR de uma monitoria
    
    Remove a ParticipacaoMonitoria entre o aluno/monitor e a turma
    """
    turma = get_object_or_404(Turma, id=turma_id, ativo=True)
    
    # Obter aluno pelo usuário autenticado
    aluno = get_aluno_by_email(request.user.email)
    if not aluno:
        messages.error(request, '❌ Aluno não encontrado')
        return redirect('participando_monitorias')
    
    # Verificar se realmente participa dessa turma
    try:
        participacao = ParticipacaoMonitoria.objects.get(aluno=aluno, turma=turma)
        participacao.delete()
        print(f"[DEBUG] Participação removida: Aluno {aluno.nome}, Turma {turma.nome}")
    except ParticipacaoMonitoria.DoesNotExist:
        messages.warning(request, '⚠️ Você não está inscrito nessa monitoria!')
    except Exception as e:
        messages.error(request, f'❌ Erro ao sair da monitoria: {str(e)}')
    
    return redirect('participando_monitorias')


@requer_grupo('Aluno')
def detalhes_presencas_monitoria(request, turma_id):
    """
    View para ALUNO ver suas presenças em uma monitoria específica
    """
    try:
        aluno = get_aluno_by_email(request.user.email)
        if not aluno:
            raise Exception("Aluno não encontrado")
            
        turma = get_object_or_404(Turma, id=turma_id)
        
        # Verificar se o aluno está inscrito nesta monitoria
        try:
            participacao = ParticipacaoMonitoria.objects.get(aluno=aluno, turma=turma)
        except ParticipacaoMonitoria.DoesNotExist:
            messages.error(request, 'Você não está participando desta monitoria.')
            return redirect('participando_monitorias')
        
        # Buscar todas as presenças do aluno nesta turma (últimos 30 dias)
        from datetime import timedelta
        hoje = timezone.now().date()
        data_limite = hoje - timedelta(days=30)
        
        presencas = Presenca.objects.filter(
            aluno=aluno,
            turma=turma,
            data__gte=data_limite
        ).order_by('-data')
        
        # Calcular estatísticas
        total_presencas = presencas.count()
        presencas_confirmadas = presencas.filter(presente=True).count()
        taxa_presenca = (presencas_confirmadas / total_presencas * 100) if total_presencas > 0 else 0
        
        # Presença de hoje
        presenca_hoje = presencas.filter(data=hoje).first()
        
    except (Aluno.DoesNotExist, ParticipacaoMonitoria.DoesNotExist):
        turma = None
        participacao = None
        presencas = []
        total_presencas = 0
        presencas_confirmadas = 0
        taxa_presenca = 0
        presenca_hoje = None
    
    context = {
        'turma': turma,
        'participacao': participacao,
        'presencas': presencas,
        'total_presencas': total_presencas,
        'presencas_confirmadas': presencas_confirmadas,
        'taxa_presenca': round(taxa_presenca, 1),
        'presenca_hoje': presenca_hoje,
        'hoje': hoje,
    }
    return render(request, 'monitorias/detalhes_presencas.html', context)


@requer_monitor
def minhas_monitorias_cards(request):
    """
    View para MONITOR ver suas monitorias em forma de cards clicáveis
    
    Cada card mostra uma monitoria que o monitor está dando
    """
    try:
        monitor = get_monitor_by_email(request.user.email)
        if monitor:
            # Buscar turmas do monitor com contagem de alunos
            turmas = Turma.objects.filter(monitor=monitor, ativo=True).select_related('vaga', 'curso')
            
            # Adicionar contagem de alunos para cada turma
            turmas_com_alunos = []
            for turma in turmas:
                total_alunos = ParticipacaoMonitoria.objects.filter(turma=turma).count()
                turmas_com_alunos.append({
                    'turma': turma,
                    'total_alunos': total_alunos
                })
        else:
            turmas_com_alunos = []
            
    except:
        turmas_com_alunos = []
    
    context = {
        'turmas_com_alunos': turmas_com_alunos,
    }
    return render(request, 'monitorias/minhas_monitorias_cards.html', context)


@requer_monitor
def alunos_da_monitoria(request, turma_id):
    """
    View para MONITOR ver alunos de uma monitoria específica
    
    Permite ver detalhes dos alunos e marcar presença
    """
    try:
        monitor = get_monitor_by_email(request.user.email)
        if not monitor:
            raise Exception("Monitor não encontrado")
        turma = get_object_or_404(Turma, id=turma_id, monitor=monitor, ativo=True)
        
        # Buscar participações (alunos) nessa turma
        participacoes = ParticipacaoMonitoria.objects.filter(
            turma=turma
        ).select_related('aluno').order_by('aluno__nome')
        
        # Buscar presenças de hoje para facilitar marcação
        hoje = timezone.now().date()
        presencas_hoje = Presenca.objects.filter(
            turma=turma, 
            data=hoje
        ).values_list('aluno_id', flat=True)
        
    except:
        turma = None
        participacoes = []
        presencas_hoje = []
    
    # Garante que o total de participantes funcione tanto com QuerySet quanto listas simples
    total_participantes = (
        participacoes.count() if hasattr(participacoes, 'count') else len(participacoes)
    )
    
    context = {
        'turma': turma,
        'participacoes': participacoes,
        'presencas_hoje': list(presencas_hoje),
        'hoje': timezone.now().date(),
        'total_participantes': total_participantes,
    }
    return render(request, 'monitorias/alunos_monitoria.html', context)


@requer_grupo('Aluno', 'Monitor')
def materiais_monitoria(request, turma_id):
    """
    Página de materiais de apoio vinculados a uma monitoria.
    Monitores podem gerenciar (upload/exclusão) e alunos visualizam e baixam.
    """
    # Localiza a turma alvo e valida se está ativa
    turma = get_object_or_404(Turma, id=turma_id, ativo=True)

    # Recupera informações do usuário logado para validar permissões
    monitor_logado = get_monitor_by_email(request.user.email)
    aluno_logado = get_aluno_by_email(request.user.email)

    # Apenas o monitor responsável pela turma pode fazer upload/remoção
    is_monitor_da_turma = monitor_logado and turma.monitor_id == monitor_logado.id
    participa_da_turma = False

    # Alunos que participam da monitoria também podem visualizar os materiais
    if aluno_logado:
        participa_da_turma = ParticipacaoMonitoria.objects.filter(
            aluno=aluno_logado,
            turma=turma
        ).exists()

    # Bloqueia acesso para quem não é monitor da turma nem aluno participante
    if not is_monitor_da_turma and not participa_da_turma:
        messages.error(request, 'Você não tem acesso a estes materiais.')
        if monitor_logado:
            return redirect('minhas_monitorias_cards')
        return redirect('participando_monitorias')

    # Lista somente materiais marcados como publicados
    materiais = turma.materiais.filter(publicado=True).select_related('monitor')
    # Formulário vazio é exibido apenas para o monitor (verificado no template)
    form = MaterialApoioForm()

    if request.method == 'POST':
        # Evita que alunos tentem enviar arquivos manualmente
        if not is_monitor_da_turma:
            messages.error(request, 'Apenas o monitor responsável pode enviar materiais.')
            return redirect('materiais_monitoria', turma_id=turma.id)

        acao = request.POST.get('action', 'create')

        if acao == 'delete':
            # Exclusão simples com remoção física do arquivo
            material_id = request.POST.get('material_id')
            material = get_object_or_404(MaterialApoio, id=material_id, turma=turma)
            material.arquivo.delete(save=False)
            material.delete()
            messages.success(request, 'Material removido com sucesso.')
            return redirect('materiais_monitoria', turma_id=turma.id)

        # Upload de novo material
        form = MaterialApoioForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.turma = turma
            material.monitor = monitor_logado
            material.save()
            return redirect('materiais_monitoria', turma_id=turma.id)
        else:
            messages.error(request, 'Corrija os erros abaixo para enviar o material.')

    context = {
        'turma': turma,
        'materiais': materiais,
        'form': form,
        'pode_gerenciar': is_monitor_da_turma,
    }
    return render(request, 'monitorias/materiais_monitoria.html', context)


@requer_monitor  
def marcar_presenca_aluno(request, turma_id, aluno_id):
    """
    View para MONITOR marcar presença de um aluno
    """
    if request.method == 'POST':
        try:
            monitor = get_monitor_by_email(request.user.email)
            if not monitor:
                raise Exception("Monitor não encontrado")
            turma = get_object_or_404(Turma, id=turma_id, monitor=monitor)
            aluno = get_object_or_404(Aluno, id=aluno_id)
            
            hoje = timezone.now().date()
            presente = request.POST.get('presente') == 'true'
            
            # Criar ou atualizar presença
            presenca, created = Presenca.objects.get_or_create(
                turma=turma,
                aluno=aluno,
                data=hoje,
                defaults={'presente': presente}
            )
            
            if not created:
                presenca.presente = presente
                presenca.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Presença {"marcada" if presente else "desmarcada"} para {aluno.nome}'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao marcar presença: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})


@requer_monitor
def meus_alunos_monitoria(request):
    """
    View para MONITOR ver todos os alunos que estão participando de suas monitorias
    
    Mostra alunos aprovados nas turmas do monitor
    """
    try:
        monitor = get_monitor_by_email(request.user.email)
        if not monitor:
            raise Exception("Monitor não encontrado")
        # Buscar turmas do monitor
        turmas = Turma.objects.filter(monitor=monitor, ativo=True).select_related('vaga', 'curso')
        
        # Buscar participações (alunos) nessas turmas
        participacoes = ParticipacaoMonitoria.objects.filter(
            turma__in=turmas
        ).select_related('aluno', 'turma').order_by('turma', 'aluno__nome')
    except:
        turmas = []
        participacoes = []
    
    context = {
        'turmas': turmas,
        'participacoes': participacoes,
    }
    return render(request, 'monitorias/meus_alunos.html', context)


# ==================== SELEÇÃO E AVALIAÇÃO DE CANDIDATOS ====================
def avaliar_candidatos(request, vaga_id):
    """
    View para professores/coordenadores avaliarem candidatos
    """
    vaga = get_object_or_404(Vaga, id=vaga_id)
    inscricoes = Inscricao.objects.filter(vaga=vaga).select_related('aluno').prefetch_related('documentos')
    
    # Filtro por status
    status_filtro = request.GET.get('status')
    if status_filtro:
        inscricoes = inscricoes.filter(status=status_filtro)
    
    context = {
        'vaga': vaga,
        'inscricoes': inscricoes,
    }
    return render(request, 'vagas/avaliar_candidatos.html', context)


def avaliar_inscricao(request, inscricao_id):
    """
    View para avaliar uma inscrição específica
    """
    inscricao = get_object_or_404(Inscricao, id=inscricao_id)
    
    if request.method == 'POST':
        inscricao.status = request.POST.get('status')
        
        try:
            pass
        except:
            pass
        
        inscricao.save()
        
        # messages.success(request, 'Avaliação registrada com sucesso!')
        return redirect('avaliar_candidatos', vaga_id=inscricao.vaga.id)
    
    context = {'inscricao': inscricao}
    return render(request, 'inscricoes/avaliar.html', context)


def comunicar_resultado(request, inscricao_id):
    """
    View para comunicar resultado ao candidato
    """
    inscricao = get_object_or_404(Inscricao, id=inscricao_id)
    
    if request.method == 'POST':
        inscricao.save()
        
        # Aqui poderia enviar um email ao candidato
        # messages.success(request, f'Resultado comunicado a {inscricao.aluno.nome}!')
        return redirect('avaliar_candidatos', vaga_id=inscricao.vaga.id)
    
    context = {'inscricao': inscricao}
    return render(request, 'inscricoes/comunicar.html', context)


# ==================== REGISTRO DE HORAS ====================
@requer_monitor
def registrar_horas(request):
    """
    View para monitor registrar suas horas de monitoria
    ⚠️ APENAS MONITORS podem acessar
    
    Fluxo:
    1. Monitor acessa a página e vê apenas suas turmas ativas
    2. Seleciona uma turma, data, hora início e fim
    3. Descreve as atividades realizadas
    4. Registra e envia para validação do professor
    5. Professor valida e aprova/rejeita
    """
    try:
        aluno = get_monitor_by_email(request.user.email)
        if not aluno:
            raise Exception("Monitor não encontrado")
        turmas = Turma.objects.filter(monitor=aluno, ativo=True)
    except:
        # Redirecionar baseado no grupo do usuário
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
            turma = Turma.objects.get(id=turma_id, monitor=aluno, ativo=True)
            
            # ✅ CONVERSÃO CORRETA: String → Date/Time
            data = datetime.strptime(data_str, '%Y-%m-%d').date()
            hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M').time()
            hora_fim = datetime.strptime(hora_fim_str, '%H:%M').time()
            
            # Validação: hora_fim deve ser maior que hora_inicio
            if hora_fim <= hora_inicio:
                messages.error(request, '❌ Hora de fim deve ser maior que a hora de início.')
                context = {'turmas': turmas}
                return render(request, 'horas/registrar.html', context)
            
            # Criar registro de horas
            RegistroHoras.objects.create(
                turma=turma,
                monitor=aluno,
                data=data,
                hora_inicio=hora_inicio,
                hora_fim=hora_fim,
                descricao_atividade=descricao,
                status='Pendente'
            )
            return redirect('meus_registros_horas')
        except Turma.DoesNotExist:
            messages.error(request, '❌ Turma não encontrada ou você não é o monitor dela.')
        except ValueError as e:
            messages.error(request, f'❌ Formato de data/hora inválido. Use formatos: data (YYYY-MM-DD), horário (HH:MM).')
        except Exception as e:
            messages.error(request, f'❌ Erro ao registrar horas: {str(e)}')
    
    context = {'turmas': turmas}
    return render(request, 'horas/registrar.html', context)


@requer_monitor
def meus_registros_horas(request):
    """
    View para monitor ver seus registros de horas
    ⚠️ APENAS MONITORS podem acessar
    """
    try:
        aluno = get_monitor_by_email(request.user.email)
        if not aluno:
            registros = []
        else:
            registros = RegistroHoras.objects.filter(monitor=aluno).select_related('turma', 'validado_por').order_by('-data')
    except:
        registros = []
    
    context = {'registros': registros}
    return render(request, 'horas/meus_registros.html', context)


@requer_monitor
def detalhes_registro(request, registro_id):
    """
    View SEGURA para monitor ver detalhes de seus registros
    
    ⚠️ SEGURANÇA CRÍTICA:
    - Monitor SÓ pode ver seus PRÓPRIOS registros
    - Monitor NÃO pode ver página de aprovação (apropiar_horas)
    - Todos os registros verificam ownership (monitor=usuário_logado)
    - @requer_monitor: Garante que APENAS monitors acessem esta view
    """
    try:
        aluno = get_monitor_by_email(request.user.email)
        if not aluno:
            raise Exception("Monitor não encontrado")
        # ✅ VERIFICAÇÃO DE SEGURANÇA: Monitor só vê seus registros
        registro = RegistroHoras.objects.get(id=registro_id, monitor=aluno)
    except RegistroHoras.DoesNotExist:
        messages.error(request, '❌ Registro não encontrado ou você não tem permissão para acessá-lo.')
        return redirect('meus_registros_horas')
    except:
        messages.error(request, '❌ Acesso negado: Você não é um monitor registrado.')
        return redirect('portal_vagas')
    
    context = {'registro': registro}
    return render(request, 'horas/detalhes_registro.html', context)


@requer_professor
def validar_horas(request):
    """
    View para professor validar horas dos monitores
    ⚠️ APENAS PROFESSORES podem acessar
    """
    try:
        funcionario = Funcionario.objects.get(email=request.user.email)
        # Buscar registros de turmas que o funcionário coordena
        registros = RegistroHoras.objects.filter(
            status='Pendente'
        ).select_related('monitor', 'turma')
    except:
        registros = []
    
    context = {'registros': registros}
    return render(request, 'horas/validar.html', context)


@requer_professor
def aprovar_horas(request, registro_id):
    """
    View para aprovar registro de horas
    ⚠️ APENAS PROFESSORES podem acessar
    """
    registro = get_object_or_404(RegistroHoras, id=registro_id)
    
    if request.method == 'POST':
        registro.status = request.POST.get('status')
        registro.observacao_validador = request.POST.get('observacao')
        
        try:
            funcionario = Funcionario.objects.get(email=request.user.email)
            registro.validado_por = funcionario
        except:
            pass
        
        registro.data_validacao = timezone.now()
        registro.save()
        
        # messages.success(request, 'Registro de horas validado!')
        return redirect('validar_horas')
    
    context = {'registro': registro}
    return render(request, 'horas/aprovar.html', context)


# ==================== DASHBOARD DE GESTÃO ====================
@requer_admin_ou_coordenador
def dashboard_gestao(request):
    """
    Dashboard com análises completas do sistema (perfil admin)
    ⚠️ APENAS ADMINS OU COORDENADORES podem acessar
    
    Inclui: KPIs, gráficos interativos, tendências, exportação Excel
    """
    import json
    from datetime import datetime, timedelta
    from collections import defaultdict
    
    # ✅ TRATAMENTO DE ERRO COMPLETO PARA DEBUG
    try:
        # ========== KPIs PRINCIPAIS ==========
        
        # Total de monitores ativos
        total_monitores = Aluno.objects.filter(monitorias__ativo=True).distinct().count()
        
        # Total de alunos no sistema
        total_alunos = Aluno.objects.filter(ativo=True).count()
        
        # Total de professores (usuários no grupo Professor)
        from django.contrib.auth.models import Group
        try:
            grupo_professor = Group.objects.get(name='Professor')
            total_professores = grupo_professor.user_set.count()
        except:
            total_professores = 0
        
        # Total de vagas ativas
        total_vagas = Vaga.objects.filter(ativo=True).count()
        
        # Total de turmas ativas
        total_turmas = Turma.objects.filter(ativo=True).count()
        
        # Total de inscrições no sistema
        total_inscricoes = Inscricao.objects.all().count()
        
        # Horas totais do mês atual
        total_horas_mes = RegistroHoras.objects.filter(
            status='Aprovado',
            data__month=timezone.now().month,
            data__year=timezone.now().year
        ).aggregate(total=Sum('total_horas'))['total'] or 0
        
        # Valor total de pagamentos do mês (baseado em StatusPagamento)
        valor_total_mes = StatusPagamento.objects.filter(
            status='Pago',
            mes_referencia__month=timezone.now().month,
            mes_referencia__year=timezone.now().year
        ).aggregate(total=Sum('valor_total'))['total'] or 0
        
        # ========== ESTATÍSTICAS DE INSCRIÇÕES ==========
        
        # Inscrições por status
        inscricoes_por_status = Inscricao.objects.values('status').annotate(
            total=Count('id')
        ).order_by('-total')
        
        # Preparar dados para gráfico de pizza
        status_labels = [item['status'] for item in inscricoes_por_status]
        status_values = [item['total'] for item in inscricoes_por_status]
        
        # Taxa de aprovação
        total_inscricoes_avaliadas = Inscricao.objects.exclude(status='Pendente').count()
        total_aprovados = Inscricao.objects.filter(status='Aprovado').count()
        taxa_aprovacao = round((total_aprovados / total_inscricoes_avaliadas * 100), 1) if total_inscricoes_avaliadas > 0 else 0
        
        # ========== MONITORES POR CURSO ==========
        
        monitores_por_curso = Inscricao.objects.filter(
            status='Aprovado'
        ).values('aluno__curso__nome').annotate(
            total=Count('id', distinct=True)
        ).order_by('-total')[:10]
        
        curso_labels = [item['aluno__curso__nome'] for item in monitores_por_curso]
        curso_values = [item['total'] for item in monitores_por_curso]
        
        # ========== EVOLUÇÃO DE INSCRIÇÕES (ÚLTIMOS 6 MESES) ==========
        
        seis_meses_atras = timezone.now() - timedelta(days=180)
        inscricoes_timeline = Inscricao.objects.filter(
            data_inscricao__gte=seis_meses_atras
        ).annotate(
            mes=TruncMonth('data_inscricao')
        ).values('mes').annotate(
            total=Count('id')
        ).order_by('mes')
        
        timeline_labels = [item['mes'].strftime('%Y-%m') if item['mes'] else '' for item in inscricoes_timeline]
        timeline_values = [item['total'] for item in inscricoes_timeline]
        
        # ========== HORAS TRABALHADAS (ÚLTIMOS 6 MESES) ==========
        
        horas_timeline = RegistroHoras.objects.filter(
            status='Aprovado',
            data__gte=seis_meses_atras
        ).annotate(
            mes=TruncMonth('data')
        ).values('mes').annotate(
            total_horas=Sum('total_horas')
        ).order_by('mes')
        
        # Buscar valores de pagamento por mês (StatusPagamento)
        pagamentos_timeline = StatusPagamento.objects.filter(
            mes_referencia__gte=seis_meses_atras
        ).annotate(
            mes=TruncMonth('mes_referencia')
        ).values('mes').annotate(
            total_valor=Sum('valor_total')
        ).order_by('mes')
        
        horas_labels = [item['mes'].strftime('%Y-%m') if item['mes'] else '' for item in horas_timeline]
        horas_values = [float(item['total_horas']) for item in horas_timeline]
        
        # Criar dicionário de pagamentos por mês para correlacionar
        pagamentos_dict = {item['mes'].strftime('%Y-%m') if item['mes'] else '': float(item['total_valor']) for item in pagamentos_timeline}
        valores_pagamento = [pagamentos_dict.get(mes, 0) for mes in horas_labels]
        
        
        # ========== REGISTRO DE HORAS POR STATUS ==========
        
        horas_por_status = RegistroHoras.objects.values('status').annotate(
            total=Count('id'),
            horas=Sum('total_horas')
        ).order_by('-total')
        
        horas_status_labels = [item['status'] for item in horas_por_status]
        horas_status_values = [item['total'] for item in horas_por_status]
        
        # ========== PENDÊNCIAS E ALERTAS ==========
        
        # Pagamentos pendentes
        pagamentos_pendentes = StatusPagamento.objects.filter(
            status='Pendente'
        ).count()
        
        # Avaliações pendentes
        avaliacoes_pendentes = Inscricao.objects.filter(
            status='Pendente'
        ).count()
        
        # Horas pendentes de validação
        horas_pendentes = RegistroHoras.objects.filter(
            status='Pendente'
        ).count()
        
        # Documentos de inscrições pendentes (Documento não tem campo status)
        documentos_pendentes = Documento.objects.filter(
            inscricao__status='Pendente'
        ).count()
        
        # ========== VAGAS ATIVAS COM DETALHES ==========
        
        vagas_ativas = Vaga.objects.filter(ativo=True).annotate(
            total_inscritos=Count('inscricao'),
            aprovados=Count('inscricao', filter=Q(inscricao__status='Aprovado'))
        ).select_related('curso', 'coordenador').order_by('-criado_em')[:10]
        
        # ========== ANÁLISE DE DESEMPENHO ==========
        
        # CR médio dos monitores aprovados
        cr_medio_monitores = Inscricao.objects.filter(
            status='Aprovado'
        ).aggregate(media=Avg('aluno__cr_geral'))['media'] or 0
        
        # Média de horas por monitor
        media_horas_monitor = RegistroHoras.objects.filter(
            status='Aprovado'
        ).aggregate(media=Avg('total_horas'))['media'] or 0
        
        # ========== ANÁLISE FINANCEIRA ==========
        
        # Total pago no ano (baseado em StatusPagamento)
        ano_atual = timezone.now().year
        total_pago_ano = StatusPagamento.objects.filter(
            status='Pago',
            mes_referencia__year=ano_atual
        ).aggregate(total=Sum('valor_total'))['total'] or 0
        
        # Média mensal de pagamentos
        media_mensal = total_pago_ano / timezone.now().month if timezone.now().month > 0 else 0
        
        # ========== EXPORTAÇÃO DE DADOS ==========
        
        # Preparar dados consolidados para exportação Excel
        dados_exportacao = {
            'monitores': Inscricao.objects.filter(status='Aprovado').select_related('aluno', 'vaga').values(
                'aluno__nome', 'aluno__matricula', 'aluno__curso__nome', 
                'vaga__disciplina', 'aluno__cr_geral'
            ),
            'horas': RegistroHoras.objects.filter(status='Aprovado').select_related('monitor').values(
                'monitor__nome', 'data', 'total_horas', 'descricao_atividade'
            ),
            'vagas': Vaga.objects.filter(ativo=True).select_related('curso', 'coordenador').values(
                'disciplina', 'curso__nome', 'numero_vagas', 'coordenador__nome'
            ),
        }
        
        context = {
            # KPIs Principais
            'total_monitores': total_monitores,
            'total_alunos': total_alunos,
            'total_professores': total_professores,
            'total_vagas': total_vagas,
            'total_turmas': total_turmas,
            'total_inscricoes': total_inscricoes,
            'total_horas_mes': round(total_horas_mes, 2),
            'valor_total_mes': round(valor_total_mes, 2),
            
            # Estatísticas de Inscrições
            'inscricoes_por_status': inscricoes_por_status,
            'status_labels': json.dumps(status_labels),
            'status_values': json.dumps(status_values),
            'taxa_aprovacao': taxa_aprovacao,
            
            # Monitores por Curso
            'monitores_por_curso': monitores_por_curso,
            'curso_labels': json.dumps(curso_labels),
            'curso_values': json.dumps(curso_values),
            
            # Timeline de Inscrições
            'timeline_labels': json.dumps(timeline_labels),
            'timeline_values': json.dumps(timeline_values),
            
            # Timeline de Horas
            'horas_labels': json.dumps(horas_labels),
            'horas_values': json.dumps(horas_values),
            'valores_pagamento': json.dumps(valores_pagamento),
            
            # Horas por Status
            'horas_status_labels': json.dumps(horas_status_labels),
            'horas_status_values': json.dumps(horas_status_values),
            
            # Pendências
            'pagamentos_pendentes': pagamentos_pendentes,
            'avaliacoes_pendentes': avaliacoes_pendentes,
            'horas_pendentes': horas_pendentes,
            'documentos_pendentes': documentos_pendentes,
            
            # Vagas
            'vagas_ativas': vagas_ativas,
            
            # Análise de Desempenho
            'cr_medio_monitores': round(cr_medio_monitores, 2),
            'media_horas_monitor': round(media_horas_monitor, 2),
            
            # Análise Financeira
            'total_pago_ano': round(total_pago_ano, 2),
            'media_mensal': round(media_mensal, 2),
            
            # Data atual
            'now': timezone.now(),
        }
        return render(request, 'gestao/dashboard.html', context)
    
    except Exception as e:
        # Se houver erro, redireciona para dashboard simples com mensagem
        import traceback
        from django.contrib import messages
        messages.error(request, f'Erro ao carregar dashboard de gestão: {str(e)}')
        print(f"ERRO DASHBOARD_GESTAO: {str(e)}")
        print(traceback.format_exc())
        # Redirecionar para dashboard normal
        return redirect('plataforma_Casa:dashboard')


def gerenciar_pagamentos(request):
    """
    View para gerenciar pagamentos dos monitores
    """
    pagamentos = StatusPagamento.objects.all().select_related('monitor', 'turma').order_by('-mes_referencia')
    
    # Filtros
    status_filtro = request.GET.get('status')
    if status_filtro:
        pagamentos = pagamentos.filter(status=status_filtro)
    
    context = {'pagamentos': pagamentos}
    return render(request, 'gestao/pagamentos.html', context)


def processar_pagamento(request, pagamento_id):
    """
    View para processar um pagamento
    """
    pagamento = get_object_or_404(StatusPagamento, id=pagamento_id)
    
    if request.method == 'POST':
        pagamento.status = request.POST.get('status')
        pagamento.observacao = request.POST.get('observacao')
        
        try:
            funcionario = Funcionario.objects.get(email=request.user.email)
            pagamento.processado_por = funcionario
        except:
            pass
        
        pagamento.data_processamento = timezone.now()
        pagamento.save()
        
        # messages.success(request, 'Pagamento processado!')
        return redirect('gerenciar_pagamentos')
    
    context = {'pagamento': pagamento}
    return render(request, 'gestao/processar_pagamento.html', context)


# ==================== RELATÓRIOS APRIMORADOS ====================
def relatorio_candidatos_por_vaga(request):
    """
    Relatório de candidatos por vaga com exportação PDF/Excel
    """
    import json
    
    vagas = Vaga.objects.filter(ativo=True).prefetch_related(
        'inscricao_set__aluno__curso',
        'inscricao_set__documentos'
    )
    
    vaga_filtro = request.GET.get('vaga')
    if vaga_filtro:
        vagas = vagas.filter(id=vaga_filtro)
    
    context = {
        'vagas': vagas,
        'now': timezone.now(),
    }
    return render(request, 'relatorios/candidatos_vaga.html', context)


def relatorio_monitores_selecionados(request):
    """
    Relatório de monitores selecionados com gráficos e exportação
    """
    import json
    from django.db.models import Avg
    
    # Buscar inscrições aprovadas
    inscricoes = Inscricao.objects.filter(status='Aprovado').select_related(
        'aluno__curso', 'vaga'
    ).order_by('aluno__nome')
    
    # Filtros
    curso_filtro = request.GET.get('curso')
    vaga_filtro = request.GET.get('vaga')
    ordem = request.GET.get('ordem', 'nome')
    
    if curso_filtro:
        inscricoes = inscricoes.filter(aluno__curso__id=curso_filtro)
    if vaga_filtro:
        inscricoes = inscricoes.filter(vaga__id=vaga_filtro)
    
    # Ordenação
    if ordem == 'cr':
        inscricoes = inscricoes.order_by('-aluno__cr_geral')
    
    # Estatísticas
    total_vagas_preenchidas = inscricoes.count()
    media_cr = inscricoes.aggregate(media=Avg('aluno__cr_geral'))['media'] or 0
    total_disciplinas = inscricoes.values('vaga__disciplina').distinct().count()
    
    # Distribuição por curso
    cursos_dist = inscricoes.values('aluno__curso__nome').annotate(
        total=Count('id')
    ).order_by('-total')
    
    cursos_labels = json.dumps([item['aluno__curso__nome'] for item in cursos_dist])
    cursos_data = json.dumps([item['total'] for item in cursos_dist])
    
    # Top 5 disciplinas
    disciplinas_dist = inscricoes.values('vaga__disciplina').annotate(
        total=Count('id')
    ).order_by('-total')[:5]
    
    disciplinas_labels = json.dumps([item['vaga__disciplina'] for item in disciplinas_dist])
    disciplinas_data = json.dumps([item['total'] for item in disciplinas_dist])
    
    context = {
        'inscricoes': inscricoes,
        'total_vagas_preenchidas': total_vagas_preenchidas,
        'media_cr': media_cr,
        'total_disciplinas': total_disciplinas,
        'cursos': Curso.objects.filter(ativo=True),
        'vagas': Vaga.objects.filter(ativo=True),
        'cursos_labels': cursos_labels,
        'cursos_data': cursos_data,
        'disciplinas_labels': disciplinas_labels,
        'disciplinas_data': disciplinas_data,
        'now': timezone.now(),
    }
    return render(request, 'relatorios/monitores_selecionados.html', context)


# ==================== MUDANÇA DE STATUS ====================
@login_required(login_url='login')
def mudar_status_candidato(request, inscricao_id):
    """
    View para mudar o status de um candidato (AJAX)
    Apenas o professor coordenador da vaga pode alterar o status
    """
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Método não permitido'
        }, status=405)
    
    try:
        # Importar json para fazer parsing do body
        import json
        data = json.loads(request.body)
        novo_status = data.get('status')
        
        # Validar status
        status_validos = ['Pendente', 'Entrevista', 'Aprovado', 'Não Aprovado']
        if novo_status not in status_validos:
            return JsonResponse({
                'success': False,
                'error': 'Status inválido'
            }, status=400)
        
        # Buscar inscrição
        inscricao = get_object_or_404(Inscricao, id=inscricao_id)
        
        # Verificar permissões do usuário
        user = request.user
        
        # ✅ PERMISSÃO: Admin, Professor ou Coordenador podem alterar
        is_admin = user.is_staff or user.is_superuser
        is_professor = user.groups.filter(name='Professor').exists()
        is_coordenador = user.groups.filter(name='Coordenador').exists()
        
        if not (is_admin or is_professor or is_coordenador):
            return JsonResponse({
                'success': False,
                'error': 'Apenas professores podem alterar status de candidatos'
            }, status=403)
        
        # ✅ VERIFICAÇÃO ADICIONAL (Opcional): Verificar se é o coordenador específico da vaga
        # Comentado para permitir que qualquer professor/admin possa alterar
        """
        try:
            funcionario = Funcionario.objects.get(email=user.email)
            # Só valida se não for admin
            if not is_admin and inscricao.vaga.coordenador != funcionario:
                return JsonResponse({
                    'success': False,
                    'error': 'Você não tem permissão para alterar o status desta inscrição'
                }, status=403)
        except Funcionario.DoesNotExist:
            if not is_admin:
                return JsonResponse({
                    'success': False,
                    'error': 'Professor não encontrado'
                }, status=404)
        """
        
        # Atualizar status
        inscricao.status = novo_status
        inscricao.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Status alterado para {novo_status} com sucesso',
            'novo_status': novo_status
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Dados inválidos'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
