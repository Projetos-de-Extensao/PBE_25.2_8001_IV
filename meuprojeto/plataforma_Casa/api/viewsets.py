from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q, Count, Avg, Sum
from django.utils import timezone
from datetime import datetime, timedelta

from ..models import (
    TipoUsuario, Curso, Sala, Disciplina, Usuario, Funcionario, Aluno,
    Vaga, Turma, ParticipacaoMonitoria, Presenca, Inscricao,
    Documento, RegistroHoras, StatusPagamento, MaterialApoio
)
from .serializers import (
    TipoUsuarioSerializer, CursoSerializer, SalaSerializer, DisciplinaSerializer, DisciplinaListSerializer,
    UsuarioSerializer, FuncionarioSerializer, FuncionarioListSerializer,
    AlunoSerializer, AlunoListSerializer,
    VagaSerializer, VagaListSerializer,
    TurmaSerializer, TurmaListSerializer,
    ParticipacaoMonitoriaSerializer, PresencaSerializer, PresencaListSerializer,
    InscricaoSerializer, InscricaoListSerializer,
    DocumentoSerializer, RegistroHorasSerializer, RegistroHorasListSerializer,
    StatusPagamentoSerializer, StatusPagamentoListSerializer,
    MaterialApoioSerializer, MaterialApoioListSerializer,
    EstatisticasSerializer
)


# ============================================================================
# VIEWSETS BASE
# ============================================================================

class TipoUsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar tipos de usuário.
    
    list: Retorna todos os tipos de usuário
    create: Cria um novo tipo de usuário
    retrieve: Retorna um tipo de usuário específico
    update: Atualiza um tipo de usuário
    partial_update: Atualiza parcialmente um tipo de usuário
    destroy: Remove um tipo de usuário
    """
    queryset = TipoUsuario.objects.all().order_by('tipo')
    serializer_class = TipoUsuarioSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['tipo']
    ordering_fields = ['tipo', 'ativo']
    ordering = ['tipo']
    
    @action(detail=False, methods=['get'])
    def ativos(self, request):
        """Lista apenas tipos de usuário ativos"""
        tipos = self.queryset.filter(ativo=True)
        serializer = self.get_serializer(tipos, many=True)
        return Response(serializer.data)


class CursoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar cursos.
    
    list: Lista todos os cursos
    create: Cria um novo curso
    retrieve: Retorna detalhes de um curso
    update: Atualiza um curso
    partial_update: Atualiza parcialmente um curso
    destroy: Remove um curso
    ativos: Lista apenas cursos ativos
    estatisticas: Estatísticas do curso
    """
    queryset = Curso.objects.all().order_by('nome')
    serializer_class = CursoSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome']
    ordering_fields = ['nome', 'ativo']
    ordering = ['nome']
    
    @action(detail=False, methods=['get'])
    def ativos(self, request):
        """Lista apenas cursos ativos"""
        cursos = self.queryset.filter(ativo=True)
        serializer = self.get_serializer(cursos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def estatisticas(self, request, pk=None):
        """Retorna estatísticas de um curso específico"""
        curso = self.get_object()
        data = {
            'curso': curso.nome,
            'total_alunos': curso.aluno_set.count(),
            'total_vagas': curso.vaga_set.count(),
            'total_turmas': curso.turma_set.count(),
            'alunos_ativos': curso.aluno_set.filter(ativo=True).count(),
            'vagas_ativas': curso.vaga_set.filter(ativo=True).count(),
        }
        return Response(data)


class SalaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar salas.
    
    list: Lista todas as salas
    create: Cria uma nova sala
    retrieve: Retorna detalhes de uma sala
    update: Atualiza uma sala
    partial_update: Atualiza parcialmente uma sala
    destroy: Remove uma sala
    disponiveis: Lista salas disponíveis
    """
    queryset = Sala.objects.all().order_by('numero')
    serializer_class = SalaSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero']
    ordering_fields = ['numero', 'ativo']
    ordering = ['numero']
    
    @action(detail=False, methods=['get'])
    def disponiveis(self, request):
        """Lista apenas salas ativas"""
        salas = self.queryset.filter(ativo=True)
        serializer = self.get_serializer(salas, many=True)
        return Response(serializer.data)


class DisciplinaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar disciplinas.
    
    list: Lista todas as disciplinas
    create: Cria uma nova disciplina (professores podem criar)
    retrieve: Retorna detalhes de uma disciplina
    update: Atualiza uma disciplina
    partial_update: Atualiza parcialmente uma disciplina
    destroy: Remove uma disciplina
    por_curso: Lista disciplinas de um curso
    por_periodo: Lista disciplinas de um período
    ativas: Lista apenas disciplinas ativas
    com_vagas: Lista disciplinas que têm vagas abertas
    """
    queryset = Disciplina.objects.select_related('curso', 'criado_por').prefetch_related('pre_requisitos').all().order_by('curso', 'periodo_sugerido', 'nome')
    serializer_class = DisciplinaSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['codigo', 'nome', 'ementa']
    ordering_fields = ['codigo', 'nome', 'periodo_sugerido', 'criado_em']
    ordering = ['curso', 'periodo_sugerido', 'nome']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DisciplinaListSerializer
        return DisciplinaSerializer
    
    def perform_create(self, serializer):
        """Ao criar, define o criador automaticamente (se autenticado)"""
        # Quando implementar autenticação, descomente:
        # serializer.save(criado_por=request.user if isinstance(request.user, Funcionario) else None)
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def por_curso(self, request):
        """Lista disciplinas de um curso específico"""
        curso_id = request.query_params.get('curso_id', None)
        if curso_id:
            disciplinas = self.queryset.filter(curso_id=curso_id)
            serializer = self.get_serializer(disciplinas, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro curso_id é obrigatório'}, status=400)
    
    @action(detail=False, methods=['get'])
    def por_periodo(self, request):
        """Lista disciplinas de um período específico"""
        periodo = request.query_params.get('periodo', None)
        if periodo:
            disciplinas = self.queryset.filter(periodo_sugerido=periodo)
            serializer = self.get_serializer(disciplinas, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro periodo é obrigatório'}, status=400)
    
    @action(detail=False, methods=['get'])
    def ativas(self, request):
        """Lista apenas disciplinas ativas"""
        disciplinas = self.queryset.filter(ativo=True)
        serializer = self.get_serializer(disciplinas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def com_vagas(self, request):
        """Lista disciplinas que têm vagas abertas"""
        disciplinas = self.queryset.filter(vagas__ativo=True).distinct()
        serializer = self.get_serializer(disciplinas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def pre_requisitos_recursivo(self, request, pk=None):
        """Retorna todos os pré-requisitos de forma recursiva"""
        disciplina = self.get_object()
        
        def get_all_pre_requisitos(disc, visited=None):
            if visited is None:
                visited = set()
            
            if disc.id in visited:
                return []
            
            visited.add(disc.id)
            pre_reqs = []
            
            for pre_req in disc.pre_requisitos.all():
                pre_reqs.append({
                    'id': pre_req.id,
                    'codigo': pre_req.codigo,
                    'nome': pre_req.nome
                })
                pre_reqs.extend(get_all_pre_requisitos(pre_req, visited))
            
            return pre_reqs
        
        pre_requisitos = get_all_pre_requisitos(disciplina)
        return Response({
            'disciplina': f"{disciplina.codigo} - {disciplina.nome}",
            'pre_requisitos': pre_requisitos
        })


# ============================================================================
# VIEWSETS DE USUÁRIOS
# ============================================================================

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar usuários base.
    
    list: Lista todos os usuários
    create: Cria um novo usuário
    retrieve: Retorna um usuário específico
    update: Atualiza um usuário
    partial_update: Atualiza parcialmente um usuário
    destroy: Remove um usuário
    """
    queryset = Usuario.objects.select_related('tipo_usuario').all().order_by('nome')
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'email']
    ordering_fields = ['nome', 'email']
    ordering = ['nome']


class FuncionarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar funcionários.
    
    list: Lista todos os funcionários
    create: Cria um novo funcionário
    retrieve: Retorna detalhes de um funcionário
    update: Atualiza um funcionário
    partial_update: Atualiza parcialmente um funcionário
    destroy: Remove um funcionário
    coordenadores: Lista apenas coordenadores
    por_departamento: Lista funcionários por departamento
    """
    queryset = Funcionario.objects.select_related('tipo_usuario').all().order_by('nome')
    serializer_class = FuncionarioSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'email', 'matricula', 'departamento', 'funcao']
    ordering_fields = ['nome', 'matricula', 'departamento']
    ordering = ['nome']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FuncionarioListSerializer
        return FuncionarioSerializer
    
    @action(detail=False, methods=['get'])
    def coordenadores(self, request):
        """Lista apenas funcionários coordenadores"""
        coordenadores = self.queryset.filter(coordenador=True)
        serializer = self.get_serializer(coordenadores, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_departamento(self, request):
        """Lista funcionários agrupados por departamento"""
        departamento = request.query_params.get('departamento', None)
        if departamento:
            funcionarios = self.queryset.filter(departamento__icontains=departamento)
            serializer = self.get_serializer(funcionarios, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro departamento é obrigatório'}, status=400)


class AlunoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar alunos.
    
    list: Lista todos os alunos
    create: Cria um novo aluno
    retrieve: Retorna detalhes de um aluno
    update: Atualiza um aluno
    partial_update: Atualiza parcialmente um aluno
    destroy: Remove um aluno
    por_curso: Lista alunos de um curso específico
    por_periodo: Lista alunos de um período específico
    monitores: Lista alunos que são monitores
    desempenho: Retorna desempenho acadêmico do aluno
    """
    queryset = Aluno.objects.select_related('curso', 'tipo_usuario').all().order_by('nome')
    serializer_class = AlunoSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'email', 'matricula']
    ordering_fields = ['nome', 'matricula', 'periodo', 'cr_geral']
    ordering = ['nome']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AlunoListSerializer
        return AlunoSerializer
    
    @action(detail=False, methods=['get'])
    def por_curso(self, request):
        """Lista alunos de um curso específico"""
        curso_id = request.query_params.get('curso_id', None)
        if curso_id:
            alunos = self.queryset.filter(curso_id=curso_id)
            serializer = self.get_serializer(alunos, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro curso_id é obrigatório'}, status=400)
    
    @action(detail=False, methods=['get'])
    def por_periodo(self, request):
        """Lista alunos de um período específico"""
        periodo = request.query_params.get('periodo', None)
        if periodo:
            alunos = self.queryset.filter(periodo=periodo)
            serializer = self.get_serializer(alunos, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro periodo é obrigatório'}, status=400)
    
    @action(detail=False, methods=['get'])
    def monitores(self, request):
        """Lista alunos que são monitores (têm turmas)"""
        monitores = self.queryset.filter(monitorias__isnull=False).distinct()
        serializer = self.get_serializer(monitores, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def desempenho(self, request, pk=None):
        """Retorna desempenho acadêmico detalhado do aluno"""
        aluno = self.get_object()
        participacoes = aluno.participacaomonitoria_set.all()
        
        data = {
            'aluno': aluno.nome,
            'cr_geral': float(aluno.cr_geral),
            'total_monitorias': participacoes.count(),
            'notas': []
        }
        
        for part in participacoes:
            data['notas'].append({
                'turma': part.turma.nome,
                'ap1': float(part.ap1) if part.ap1 else None,
                'ap2': float(part.ap2) if part.ap2 else None,
                'cr': float(part.cr) if part.cr else None,
            })
        
        return Response(data)


# ============================================================================
# VIEWSETS DE VAGAS E TURMAS
# ============================================================================

class VagaViewSet(viewsets.ModelViewSet):
    """
    API endpoint completo para vagas de monitoria.
    
    list: Lista todas as vagas
    create: Cria uma nova vaga
    retrieve: Retorna detalhes de uma vaga
    update: Atualiza uma vaga
    partial_update: Atualiza parcialmente uma vaga
    destroy: Remove uma vaga
    ativas: Lista vagas ativas
    por_curso: Lista vagas de um curso
    com_vagas_disponiveis: Lista vagas com vagas disponíveis
    inscricoes: Lista inscrições de uma vaga
    """
    queryset = Vaga.objects.select_related('curso', 'coordenador').prefetch_related('monitores').all().order_by('-criado_em')
    serializer_class = VagaSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao', 'requisitos', 'disciplina']
    ordering_fields = ['criado_em', 'numero_vagas', 'nome']
    ordering = ['-criado_em']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return VagaListSerializer
        return VagaSerializer
    
    @action(detail=False, methods=['get'])
    def ativas(self, request):
        """Lista apenas vagas ativas"""
        vagas = self.queryset.filter(ativo=True)
        serializer = self.get_serializer(vagas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_curso(self, request):
        """Lista vagas de um curso específico"""
        curso_id = request.query_params.get('curso_id', None)
        if curso_id:
            vagas = self.queryset.filter(curso_id=curso_id)
            serializer = self.get_serializer(vagas, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro curso_id é obrigatório'}, status=400)
    
    @action(detail=False, methods=['get'])
    def com_vagas_disponiveis(self, request):
        """Lista vagas que ainda têm vagas disponíveis"""
        vagas_disponiveis = []
        for vaga in self.queryset.filter(ativo=True):
            if vaga.vagas_disponiveis() > 0:
                vagas_disponiveis.append(vaga)
        serializer = self.get_serializer(vagas_disponiveis, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def inscricoes(self, request, pk=None):
        """Lista todas as inscrições de uma vaga"""
        vaga = self.get_object()
        inscricoes = vaga.inscricao_set.all()
        serializer = InscricaoSerializer(inscricoes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def adicionar_coordenador(self, request, pk=None):
        """Adiciona um coordenador à vaga"""
        vaga = self.get_object()
        coordenador_id = request.data.get('coordenador_id')
        
        if not coordenador_id:
            return Response({'error': 'coordenador_id é obrigatório'}, status=400)
        
        try:
            coordenador = Funcionario.objects.get(id=coordenador_id, coordenador=True)
            vaga.coordenadores.add(coordenador)
            return Response({'message': 'Coordenador adicionado com sucesso'})
        except Funcionario.DoesNotExist:
            return Response({'error': 'Coordenador não encontrado'}, status=404)
    
    @action(detail=True, methods=['post'])
    def remover_coordenador(self, request, pk=None):
        """Remove um coordenador da vaga"""
        vaga = self.get_object()
        coordenador_id = request.data.get('coordenador_id')
        
        if not coordenador_id:
            return Response({'error': 'coordenador_id é obrigatório'}, status=400)
        
        try:
            coordenador = Funcionario.objects.get(id=coordenador_id)
            vaga.coordenadores.remove(coordenador)
            return Response({'message': 'Coordenador removido com sucesso'})
        except Funcionario.DoesNotExist:
            return Response({'error': 'Coordenador não encontrado'}, status=404)
    
    @action(detail=True, methods=['post'])
    def adicionar_professor(self, request, pk=None):
        """Adiciona um professor à vaga"""
        vaga = self.get_object()
        professor_id = request.data.get('professor_id')
        
        if not professor_id:
            return Response({'error': 'professor_id é obrigatório'}, status=400)
        
        try:
            professor = Funcionario.objects.get(id=professor_id, funcao='Professor')
            vaga.professores.add(professor)
            return Response({'message': 'Professor adicionado com sucesso'})
        except Funcionario.DoesNotExist:
            return Response({'error': 'Professor não encontrado'}, status=404)
    
    @action(detail=True, methods=['post'])
    def remover_professor(self, request, pk=None):
        """Remove um professor da vaga"""
        vaga = self.get_object()
        professor_id = request.data.get('professor_id')
        
        if not professor_id:
            return Response({'error': 'professor_id é obrigatório'}, status=400)
        
        try:
            professor = Funcionario.objects.get(id=professor_id)
            vaga.professores.remove(professor)
            return Response({'message': 'Professor removido com sucesso'})
        except Funcionario.DoesNotExist:
            return Response({'error': 'Professor não encontrado'}, status=404)


class TurmaViewSet(viewsets.ModelViewSet):
    """
    API endpoint completo para turmas de monitoria.
    
    list: Lista todas as turmas
    create: Cria uma nova turma
    retrieve: Retorna detalhes de uma turma
    update: Atualiza uma turma
    partial_update: Atualiza parcialmente uma turma
    destroy: Remove uma turma
    ativas: Lista turmas ativas
    por_monitor: Lista turmas de um monitor
    por_periodo: Lista turmas em um período
    participantes: Lista participantes de uma turma
    presencas: Lista presenças de uma turma
    materiais: Lista materiais de uma turma
    """
    queryset = Turma.objects.select_related('vaga', 'sala', 'monitor', 'curso').all().order_by('nome')
    serializer_class = TurmaSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao', 'dias_da_semana', 'horario']
    ordering_fields = ['nome', 'data_inicio', 'data_fim']
    ordering = ['nome']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TurmaListSerializer
        return TurmaSerializer
    
    @action(detail=False, methods=['get'])
    def ativas(self, request):
        """Lista apenas turmas ativas"""
        turmas = self.queryset.filter(ativo=True)
        serializer = self.get_serializer(turmas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_monitor(self, request):
        """Lista turmas de um monitor específico"""
        monitor_id = request.query_params.get('monitor_id', None)
        if monitor_id:
            turmas = self.queryset.filter(monitor_id=monitor_id)
            serializer = self.get_serializer(turmas, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro monitor_id é obrigatório'}, status=400)
    
    @action(detail=False, methods=['get'])
    def por_periodo(self, request):
        """Lista turmas que estão ativas em um período"""
        data_atual = timezone.now().date()
        turmas = self.queryset.filter(
            data_inicio__lte=data_atual,
            data_fim__gte=data_atual,
            ativo=True
        )
        serializer = self.get_serializer(turmas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def participantes(self, request, pk=None):
        """Lista participantes de uma turma"""
        turma = self.get_object()
        participacoes = turma.participacaomonitoria_set.all()
        serializer = ParticipacaoMonitoriaSerializer(participacoes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def presencas(self, request, pk=None):
        """Lista presenças de uma turma"""
        turma = self.get_object()
        presencas = turma.presenca_set.all().order_by('-data')
        serializer = PresencaSerializer(presencas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def materiais(self, request, pk=None):
        """Lista materiais de apoio de uma turma"""
        turma = self.get_object()
        materiais = turma.materiais.all().order_by('-criado_em')
        serializer = MaterialApoioSerializer(materiais, many=True)
        return Response(serializer.data)


# ============================================================================
# VIEWSETS DE PARTICIPAÇÃO E PRESENÇA
# ============================================================================

class ParticipacaoMonitoriaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para participação em monitorias.
    
    list: Lista todas as participações
    create: Registra nova participação
    retrieve: Retorna detalhes de uma participação
    update: Atualiza uma participação
    partial_update: Atualiza parcialmente uma participação
    destroy: Remove uma participação
    por_aluno: Lista participações de um aluno
    por_turma: Lista participações de uma turma
    """
    queryset = ParticipacaoMonitoria.objects.select_related('aluno', 'turma').all()
    serializer_class = ParticipacaoMonitoriaSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['aluno__nome', 'turma__nome']
    ordering_fields = ['aluno__nome', 'turma__nome']
    
    @action(detail=False, methods=['get'])
    def por_aluno(self, request):
        """Lista participações de um aluno específico"""
        aluno_id = request.query_params.get('aluno_id', None)
        if aluno_id:
            participacoes = self.queryset.filter(aluno_id=aluno_id)
            serializer = self.get_serializer(participacoes, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro aluno_id é obrigatório'}, status=400)
    
    @action(detail=False, methods=['get'])
    def por_turma(self, request):
        """Lista participações de uma turma específica"""
        turma_id = request.query_params.get('turma_id', None)
        if turma_id:
            participacoes = self.queryset.filter(turma_id=turma_id)
            serializer = self.get_serializer(participacoes, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro turma_id é obrigatório'}, status=400)


class PresencaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para registro de presenças.
    
    list: Lista todos os registros de presença
    create: Registra nova presença
    retrieve: Retorna detalhes de uma presença
    update: Atualiza uma presença
    partial_update: Atualiza parcialmente uma presença
    destroy: Remove uma presença
    por_aluno: Lista presenças de um aluno
    por_turma: Lista presenças de uma turma
    por_data: Lista presenças em uma data
    taxa_presenca: Calcula taxa de presença
    """
    queryset = Presenca.objects.select_related('turma', 'aluno').all().order_by('-data')
    serializer_class = PresencaSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['aluno__nome', 'turma__nome']
    ordering_fields = ['data', 'aluno__nome']
    ordering = ['-data']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PresencaListSerializer
        return PresencaSerializer
    
    @action(detail=False, methods=['get'])
    def por_aluno(self, request):
        """Lista presenças de um aluno específico"""
        aluno_id = request.query_params.get('aluno_id', None)
        if aluno_id:
            presencas = self.queryset.filter(aluno_id=aluno_id)
            serializer = self.get_serializer(presencas, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro aluno_id é obrigatório'}, status=400)
    
    @action(detail=False, methods=['get'])
    def por_turma(self, request):
        """Lista presenças de uma turma específica"""
        turma_id = request.query_params.get('turma_id', None)
        if turma_id:
            presencas = self.queryset.filter(turma_id=turma_id)
            serializer = self.get_serializer(presencas, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro turma_id é obrigatório'}, status=400)
    
    @action(detail=False, methods=['get'])
    def por_data(self, request):
        """Lista presenças em uma data específica"""
        data = request.query_params.get('data', None)
        if data:
            presencas = self.queryset.filter(data=data)
            serializer = self.get_serializer(presencas, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro data é obrigatório (formato: YYYY-MM-DD)'}, status=400)
    
    @action(detail=False, methods=['get'])
    def taxa_presenca(self, request):
        """Calcula taxa de presença por aluno ou turma"""
        aluno_id = request.query_params.get('aluno_id', None)
        turma_id = request.query_params.get('turma_id', None)
        
        if aluno_id:
            total = self.queryset.filter(aluno_id=aluno_id).count()
            presentes = self.queryset.filter(aluno_id=aluno_id, presente=True).count()
        elif turma_id:
            total = self.queryset.filter(turma_id=turma_id).count()
            presentes = self.queryset.filter(turma_id=turma_id, presente=True).count()
        else:
            return Response({'error': 'Informe aluno_id ou turma_id'}, status=400)
        
        taxa = (presentes / total * 100) if total > 0 else 0
        return Response({
            'total_registros': total,
            'total_presencas': presentes,
            'taxa_presenca': round(taxa, 2)
        })


# ============================================================================
# VIEWSETS DE INSCRIÇÕES E DOCUMENTOS
# ============================================================================

class InscricaoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para inscrições em vagas.
    
    list: Lista todas as inscrições
    create: Cria nova inscrição
    retrieve: Retorna detalhes de uma inscrição
    update: Atualiza uma inscrição
    partial_update: Atualiza parcialmente uma inscrição
    destroy: Remove uma inscrição
    por_status: Lista inscrições por status
    por_aluno: Lista inscrições de um aluno
    por_vaga: Lista inscrições de uma vaga
    aprovar: Aprova uma inscrição
    rejeitar: Rejeita uma inscrição
    """
    queryset = Inscricao.objects.select_related('aluno', 'vaga').all().order_by('-data_inscricao')
    serializer_class = InscricaoSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['aluno__nome', 'vaga__nome', 'status']
    ordering_fields = ['data_inscricao', 'status']
    ordering = ['-data_inscricao']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return InscricaoListSerializer
        return InscricaoSerializer
    
    @action(detail=False, methods=['get'])
    def por_status(self, request):
        """Lista inscrições por status"""
        status_param = request.query_params.get('status', None)
        if status_param:
            inscricoes = self.queryset.filter(status=status_param)
            serializer = self.get_serializer(inscricoes, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro status é obrigatório'}, status=400)
    
    @action(detail=False, methods=['get'])
    def por_aluno(self, request):
        """Lista inscrições de um aluno"""
        aluno_id = request.query_params.get('aluno_id', None)
        if aluno_id:
            inscricoes = self.queryset.filter(aluno_id=aluno_id)
            serializer = self.get_serializer(inscricoes, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro aluno_id é obrigatório'}, status=400)
    
    @action(detail=False, methods=['get'])
    def por_vaga(self, request):
        """Lista inscrições de uma vaga"""
        vaga_id = request.query_params.get('vaga_id', None)
        if vaga_id:
            inscricoes = self.queryset.filter(vaga_id=vaga_id)
            serializer = self.get_serializer(inscricoes, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro vaga_id é obrigatório'}, status=400)
    
    @action(detail=True, methods=['post'])
    def aprovar(self, request, pk=None):
        """Aprova uma inscrição"""
        inscricao = self.get_object()
        inscricao.status = 'Aprovado'
        inscricao.save()
        serializer = self.get_serializer(inscricao)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def rejeitar(self, request, pk=None):
        """Rejeita uma inscrição"""
        inscricao = self.get_object()
        inscricao.status = 'Não Aprovado'
        inscricao.save()
        serializer = self.get_serializer(inscricao)
        return Response(serializer.data)


class DocumentoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para documentos de inscrição.
    
    list: Lista todos os documentos
    create: Faz upload de novo documento
    retrieve: Retorna detalhes de um documento
    update: Atualiza um documento
    partial_update: Atualiza parcialmente um documento
    destroy: Remove um documento
    por_inscricao: Lista documentos de uma inscrição
    por_tipo: Lista documentos por tipo
    """
    queryset = Documento.objects.select_related('inscricao__aluno', 'inscricao__vaga').all().order_by('-enviado_em')
    serializer_class = DocumentoSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['tipo', 'nome_arquivo', 'inscricao__aluno__nome']
    ordering_fields = ['enviado_em', 'tipo']
    ordering = ['-enviado_em']
    
    @action(detail=False, methods=['get'])
    def por_inscricao(self, request):
        """Lista documentos de uma inscrição"""
        inscricao_id = request.query_params.get('inscricao_id', None)
        if inscricao_id:
            documentos = self.queryset.filter(inscricao_id=inscricao_id)
            serializer = self.get_serializer(documentos, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro inscricao_id é obrigatório'}, status=400)
    
    @action(detail=False, methods=['get'])
    def por_tipo(self, request):
        """Lista documentos por tipo"""
        tipo = request.query_params.get('tipo', None)
        if tipo:
            documentos = self.queryset.filter(tipo=tipo)
            serializer = self.get_serializer(documentos, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro tipo é obrigatório'}, status=400)


# ============================================================================
# VIEWSETS DE HORAS E PAGAMENTOS
# ============================================================================

class RegistroHorasViewSet(viewsets.ModelViewSet):
    """
    API endpoint para registro de horas trabalhadas.
    
    list: Lista todos os registros de horas
    create: Cria novo registro de horas
    retrieve: Retorna detalhes de um registro
    update: Atualiza um registro
    partial_update: Atualiza parcialmente um registro
    destroy: Remove um registro
    por_monitor: Lista registros de um monitor
    por_turma: Lista registros de uma turma
    por_status: Lista registros por status
    pendentes: Lista registros pendentes
    aprovar: Aprova um registro
    rejeitar: Rejeita um registro
    total_horas_monitor: Total de horas de um monitor
    """
    queryset = RegistroHoras.objects.select_related('turma', 'monitor', 'validado_por').all().order_by('-data')
    serializer_class = RegistroHorasSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['monitor__nome', 'turma__nome', 'status']
    ordering_fields = ['data', 'total_horas', 'status']
    ordering = ['-data']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RegistroHorasListSerializer
        return RegistroHorasSerializer
    
    @action(detail=False, methods=['get'])
    def por_monitor(self, request):
        """Lista registros de um monitor"""
        monitor_id = request.query_params.get('monitor_id', None)
        if monitor_id:
            registros = self.queryset.filter(monitor_id=monitor_id)
            serializer = self.get_serializer(registros, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro monitor_id é obrigatório'}, status=400)
    
    @action(detail=False, methods=['get'])
    def por_turma(self, request):
        """Lista registros de uma turma"""
        turma_id = request.query_params.get('turma_id', None)
        if turma_id:
            registros = self.queryset.filter(turma_id=turma_id)
            serializer = self.get_serializer(registros, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro turma_id é obrigatório'}, status=400)
    
    @action(detail=False, methods=['get'])
    def por_status(self, request):
        """Lista registros por status"""
        status_param = request.query_params.get('status', None)
        if status_param:
            registros = self.queryset.filter(status=status_param)
            serializer = self.get_serializer(registros, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro status é obrigatório'}, status=400)
    
    @action(detail=False, methods=['get'])
    def pendentes(self, request):
        """Lista apenas registros pendentes"""
        registros = self.queryset.filter(status='Pendente')
        serializer = self.get_serializer(registros, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def aprovar(self, request, pk=None):
        """Aprova um registro de horas"""
        registro = self.get_object()
        registro.status = 'Aprovado'
        registro.data_validacao = timezone.now()
        # registro.validado_por = request.user  # Descomente se tiver autenticação
        registro.save()
        serializer = self.get_serializer(registro)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def rejeitar(self, request, pk=None):
        """Rejeita um registro de horas"""
        registro = self.get_object()
        registro.status = 'Rejeitado'
        registro.data_validacao = timezone.now()
        registro.observacao_validador = request.data.get('observacao', '')
        # registro.validado_por = request.user  # Descomente se tiver autenticação
        registro.save()
        serializer = self.get_serializer(registro)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def total_horas_monitor(self, request):
        """Calcula total de horas aprovadas de um monitor"""
        monitor_id = request.query_params.get('monitor_id', None)
        if not monitor_id:
            return Response({'error': 'Parâmetro monitor_id é obrigatório'}, status=400)
        
        registros = self.queryset.filter(monitor_id=monitor_id, status='Aprovado')
        total = registros.aggregate(total=Sum('total_horas'))['total'] or 0
        
        return Response({
            'monitor_id': monitor_id,
            'total_registros': registros.count(),
            'total_horas': float(total)
        })


class StatusPagamentoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para status de pagamento.
    
    list: Lista todos os pagamentos
    create: Cria novo registro de pagamento
    retrieve: Retorna detalhes de um pagamento
    update: Atualiza um pagamento
    partial_update: Atualiza parcialmente um pagamento
    destroy: Remove um pagamento
    por_monitor: Lista pagamentos de um monitor
    por_status: Lista pagamentos por status
    pendentes: Lista pagamentos pendentes
    processar: Processa um pagamento
    """
    queryset = StatusPagamento.objects.select_related('monitor', 'turma', 'processado_por').all().order_by('-mes_referencia')
    serializer_class = StatusPagamentoSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['monitor__nome', 'turma__nome', 'status']
    ordering_fields = ['mes_referencia', 'valor_total', 'status']
    ordering = ['-mes_referencia']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return StatusPagamentoListSerializer
        return StatusPagamentoSerializer
    
    @action(detail=False, methods=['get'])
    def por_monitor(self, request):
        """Lista pagamentos de um monitor"""
        monitor_id = request.query_params.get('monitor_id', None)
        if monitor_id:
            pagamentos = self.queryset.filter(monitor_id=monitor_id)
            serializer = self.get_serializer(pagamentos, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro monitor_id é obrigatório'}, status=400)
    
    @action(detail=False, methods=['get'])
    def por_status(self, request):
        """Lista pagamentos por status"""
        status_param = request.query_params.get('status', None)
        if status_param:
            pagamentos = self.queryset.filter(status=status_param)
            serializer = self.get_serializer(pagamentos, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro status é obrigatório'}, status=400)
    
    @action(detail=False, methods=['get'])
    def pendentes(self, request):
        """Lista apenas pagamentos pendentes"""
        pagamentos = self.queryset.filter(status='Pendente')
        serializer = self.get_serializer(pagamentos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def processar(self, request, pk=None):
        """Processa um pagamento"""
        pagamento = self.get_object()
        pagamento.status = 'Pago'
        pagamento.data_processamento = timezone.now()
        # pagamento.processado_por = request.user  # Descomente se tiver autenticação
        pagamento.save()
        serializer = self.get_serializer(pagamento)
        return Response(serializer.data)


# ============================================================================
# VIEWSETS DE MATERIAIS
# ============================================================================

class MaterialApoioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para materiais de apoio.
    
    list: Lista todos os materiais
    create: Faz upload de novo material
    retrieve: Retorna detalhes de um material
    update: Atualiza um material
    partial_update: Atualiza parcialmente um material
    destroy: Remove um material
    por_turma: Lista materiais de uma turma
    por_tipo: Lista materiais por tipo
    publicados: Lista apenas materiais publicados
    """
    queryset = MaterialApoio.objects.select_related('turma', 'monitor').all().order_by('-criado_em')
    serializer_class = MaterialApoioSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titulo', 'descricao', 'tipo']
    ordering_fields = ['criado_em', 'atualizado_em', 'tipo']
    ordering = ['-criado_em']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MaterialApoioListSerializer
        return MaterialApoioSerializer
    
    @action(detail=False, methods=['get'])
    def por_turma(self, request):
        """Lista materiais de uma turma"""
        turma_id = request.query_params.get('turma_id', None)
        if turma_id:
            materiais = self.queryset.filter(turma_id=turma_id)
            serializer = self.get_serializer(materiais, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro turma_id é obrigatório'}, status=400)
    
    @action(detail=False, methods=['get'])
    def por_tipo(self, request):
        """Lista materiais por tipo"""
        tipo = request.query_params.get('tipo', None)
        if tipo:
            materiais = self.queryset.filter(tipo=tipo)
            serializer = self.get_serializer(materiais, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parâmetro tipo é obrigatório'}, status=400)
    
    @action(detail=False, methods=['get'])
    def publicados(self, request):
        """Lista apenas materiais publicados"""
        materiais = self.queryset.filter(publicado=True)
        serializer = self.get_serializer(materiais, many=True)
        return Response(serializer.data)


# ============================================================================
# VIEWSET DE ESTATÍSTICAS
# ============================================================================

class EstatisticasViewSet(viewsets.ViewSet):
    """
    API endpoint para estatísticas do sistema.
    
    geral: Estatísticas gerais do sistema
    por_curso: Estatísticas de um curso
    por_periodo: Estatísticas de um período
    """
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def geral(self, request):
        """Retorna estatísticas gerais do sistema"""
        data = {
            'total_alunos': Aluno.objects.count(),
            'total_funcionarios': Funcionario.objects.count(),
            'total_vagas': Vaga.objects.count(),
            'total_turmas': Turma.objects.count(),
            'total_inscricoes': Inscricao.objects.count(),
            'vagas_ativas': Vaga.objects.filter(ativo=True).count(),
            'turmas_ativas': Turma.objects.filter(ativo=True).count(),
            'inscricoes_pendentes': Inscricao.objects.filter(status='Pendente').count(),
            'inscricoes_aprovadas': Inscricao.objects.filter(status='Aprovado').count(),
            'total_presencas': Presenca.objects.filter(presente=True).count(),
            'total_materiais': MaterialApoio.objects.filter(publicado=True).count(),
        }
        serializer = EstatisticasSerializer(data)
        return Response(serializer.data)
