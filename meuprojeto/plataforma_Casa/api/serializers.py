from rest_framework import serializers
from decimal import Decimal

from ..models import (
    TipoUsuario, Curso, Sala, Disciplina, Usuario, Funcionario, Aluno,
    Vaga, Turma, ParticipacaoMonitoria, Presenca, Inscricao,
    Documento, RegistroHoras, StatusPagamento, MaterialApoio
)


# ============================================================================
# SERIALIZERS BASE
# ============================================================================

class TipoUsuarioSerializer(serializers.ModelSerializer):
    """Serializer para tipos de usuário do sistema"""
    
    class Meta:
        model = TipoUsuario
        fields = ['id', 'tipo', 'ativo']
        

class CursoSerializer(serializers.ModelSerializer):
    """Serializer para cursos disponíveis"""
    total_alunos = serializers.SerializerMethodField()
    total_vagas = serializers.SerializerMethodField()
    
    class Meta:
        model = Curso
        fields = ['id', 'nome', 'ativo', 'total_alunos', 'total_vagas']
    
    def get_total_alunos(self, obj):
        return obj.aluno_set.count()
    
    def get_total_vagas(self, obj):
        return obj.vaga_set.count()


class SalaSerializer(serializers.ModelSerializer):
    """Serializer para salas disponíveis"""
    total_turmas = serializers.SerializerMethodField()
    
    class Meta:
        model = Sala
        fields = ['id', 'numero', 'ativo', 'total_turmas']
    
    def get_total_turmas(self, obj):
        return obj.turma_set.count()


class DisciplinaSerializer(serializers.ModelSerializer):
    """Serializer completo para disciplinas"""
    curso_nome = serializers.CharField(source='curso.nome', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.nome', read_only=True)
    total_vagas = serializers.SerializerMethodField()
    pre_requisitos_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Disciplina
        fields = [
            'id', 'codigo', 'nome', 'curso', 'curso_nome', 
            'carga_horaria', 'periodo_sugerido', 'ementa',
            'pre_requisitos', 'pre_requisitos_info',
            'criado_por', 'criado_por_nome', 
            'criado_em', 'atualizado_em', 'ativo', 'total_vagas'
        ]
        read_only_fields = ['criado_em', 'atualizado_em']
    
    def get_total_vagas(self, obj):
        return obj.vagas.count()
    
    def get_pre_requisitos_info(self, obj):
        return [{'id': d.id, 'codigo': d.codigo, 'nome': d.nome} 
                for d in obj.pre_requisitos.all()]


class DisciplinaListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de disciplinas"""
    curso_nome = serializers.CharField(source='curso.nome', read_only=True)
    
    class Meta:
        model = Disciplina
        fields = ['id', 'codigo', 'nome', 'curso_nome', 'periodo_sugerido', 'ativo']


# ============================================================================
# SERIALIZERS DE USUÁRIOS
# ============================================================================

class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer base para usuários"""
    tipo_usuario_nome = serializers.CharField(source='tipo_usuario.tipo', read_only=True)
    
    class Meta:
        model = Usuario
        fields = [
            'id', 'nome', 'email', 'tipo_usuario', 'tipo_usuario_nome', 'ativo'
        ]


class FuncionarioSerializer(serializers.ModelSerializer):
    """Serializer completo para funcionários"""
    tipo_usuario_nome = serializers.CharField(source='tipo_usuario.tipo', read_only=True)
    total_vagas_coordenadas = serializers.SerializerMethodField()
    total_horas_validadas = serializers.SerializerMethodField()
    
    class Meta:
        model = Funcionario
        fields = [
            'id', 'nome', 'email', 'tipo_usuario', 'tipo_usuario_nome',
            'matricula', 'departamento', 'funcao', 'coordenador', 'ativo',
            'total_vagas_coordenadas', 'total_horas_validadas'
        ]
    
    def get_total_vagas_coordenadas(self, obj):
        return obj.vagas_coordenadas.count()
    
    def get_total_horas_validadas(self, obj):
        return obj.horas_validadas.count()


class FuncionarioListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de funcionários"""
    tipo_usuario_nome = serializers.CharField(source='tipo_usuario.tipo', read_only=True)
    
    class Meta:
        model = Funcionario
        fields = ['id', 'nome', 'email', 'matricula', 'funcao', 'tipo_usuario_nome', 'ativo']


class AlunoSerializer(serializers.ModelSerializer):
    """Serializer completo para alunos"""
    curso_nome = serializers.CharField(source='curso.nome', read_only=True)
    tipo_usuario_nome = serializers.CharField(source='tipo_usuario.tipo', read_only=True)
    total_inscricoes = serializers.SerializerMethodField()
    total_turmas_monitor = serializers.SerializerMethodField()
    total_presencas = serializers.SerializerMethodField()
    
    class Meta:
        model = Aluno
        fields = [
            'id', 'nome', 'email', 'tipo_usuario', 'tipo_usuario_nome',
            'matricula', 'curso', 'curso_nome', 'data_ingresso',
            'periodo', 'cr_geral', 'ativo',
            'total_inscricoes', 'total_turmas_monitor', 'total_presencas'
        ]
    
    def get_total_inscricoes(self, obj):
        return obj.inscricao_set.count()
    
    def get_total_turmas_monitor(self, obj):
        return obj.monitorias.count()
    
    def get_total_presencas(self, obj):
        return obj.presenca_set.filter(presente=True).count()


class AlunoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de alunos"""
    curso_nome = serializers.CharField(source='curso.nome', read_only=True)
    
    class Meta:
        model = Aluno
        fields = [
            'id', 'nome', 'email', 'matricula', 'curso', 'curso_nome',
            'periodo', 'cr_geral', 'ativo'
        ]


# ============================================================================
# SERIALIZERS DE VAGAS E TURMAS
# ============================================================================

class VagaSerializer(serializers.ModelSerializer):
    """Serializer completo para vagas"""
    curso_nome = serializers.CharField(source='curso.nome', read_only=True)
    disciplina_info = serializers.SerializerMethodField()
    coordenadores_info = FuncionarioListSerializer(source='coordenadores', many=True, read_only=True)
    professores_info = FuncionarioListSerializer(source='professores', many=True, read_only=True)
    vagas_disponiveis = serializers.SerializerMethodField()
    total_inscricoes = serializers.SerializerMethodField()
    total_turmas = serializers.SerializerMethodField()
    monitores_info = AlunoListSerializer(source='monitores', many=True, read_only=True)
    tipo_vaga_display = serializers.CharField(source='get_tipo_vaga_display', read_only=True)
    
    class Meta:
        model = Vaga
        fields = [
            'id', 'nome', 'descricao', 'requisitos', 'responsabilidades',
            'numero_vagas', 'disciplina', 'disciplina_info', 'ativo', 'criado_em',
            'curso', 'curso_nome', 
            'tipo_vaga', 'tipo_vaga_display', 'valor_bolsa',
            'coordenadores', 'coordenadores_info',
            'professores', 'professores_info',
            'vagas_disponiveis', 'total_inscricoes', 'total_turmas',
            'monitores_info'
        ]
    
    def get_disciplina_info(self, obj):
        if obj.disciplina:
            return {
                'id': obj.disciplina.id,
                'codigo': obj.disciplina.codigo,
                'nome': obj.disciplina.nome
            }
        return None
    
    def get_vagas_disponiveis(self, obj):
        return obj.vagas_disponiveis()
    
    def get_total_inscricoes(self, obj):
        return obj.inscricao_set.count()
    
    def get_total_turmas(self, obj):
        return obj.turma_set.count()


class VagaListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de vagas"""
    curso_nome = serializers.CharField(source='curso.nome', read_only=True)
    disciplina_nome = serializers.CharField(source='disciplina.nome', read_only=True)
    vagas_disponiveis = serializers.SerializerMethodField()
    total_coordenadores = serializers.SerializerMethodField()
    total_professores = serializers.SerializerMethodField()
    tipo_vaga_display = serializers.CharField(source='get_tipo_vaga_display', read_only=True)
    
    class Meta:
        model = Vaga
        fields = [
            'id', 'nome', 'curso_nome', 'disciplina_nome', 'numero_vagas',
            'tipo_vaga', 'tipo_vaga_display', 'valor_bolsa',
            'vagas_disponiveis', 'total_coordenadores', 'total_professores',
            'ativo', 'criado_em'
        ]
    
    def get_vagas_disponiveis(self, obj):
        return obj.vagas_disponiveis()
    
    def get_total_coordenadores(self, obj):
        return obj.coordenadores.count()
    
    def get_total_professores(self, obj):
        return obj.professores.count()


class TurmaSerializer(serializers.ModelSerializer):
    """Serializer completo para turmas"""
    vaga_nome = serializers.CharField(source='vaga.nome', read_only=True)
    sala_numero = serializers.CharField(source='sala.numero', read_only=True)
    monitor_nome = serializers.CharField(source='monitor.nome', read_only=True)
    curso_nome = serializers.CharField(source='curso.nome', read_only=True)
    total_participantes = serializers.SerializerMethodField()
    total_presencas = serializers.SerializerMethodField()
    total_materiais = serializers.SerializerMethodField()
    
    class Meta:
        model = Turma
        fields = [
            'id', 'nome', 'descricao', 'data_inicio', 'data_fim',
            'dias_da_semana', 'horario', 'ativo', 'criado_em',
            'vaga', 'vaga_nome', 'sala', 'sala_numero',
            'monitor', 'monitor_nome', 'curso', 'curso_nome',
            'total_participantes', 'total_presencas', 'total_materiais'
        ]
    
    def get_total_participantes(self, obj):
        return obj.participacaomonitoria_set.count()
    
    def get_total_presencas(self, obj):
        return obj.presenca_set.count()
    
    def get_total_materiais(self, obj):
        return obj.materiais.count()


class TurmaListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de turmas"""
    vaga_nome = serializers.CharField(source='vaga.nome', read_only=True)
    monitor_nome = serializers.CharField(source='monitor.nome', read_only=True)
    
    class Meta:
        model = Turma
        fields = [
            'id', 'nome', 'vaga_nome', 'monitor_nome',
            'data_inicio', 'data_fim', 'ativo'
        ]


# ============================================================================
# SERIALIZERS DE PARTICIPAÇÃO E PRESENÇA
# ============================================================================

class ParticipacaoMonitoriaSerializer(serializers.ModelSerializer):
    """Serializer para participação de alunos em monitorias"""
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    media_final = serializers.SerializerMethodField()
    
    class Meta:
        model = ParticipacaoMonitoria
        fields = [
            'id', 'aluno', 'aluno_nome', 'turma', 'turma_nome',
            'ap1', 'ap2', 'cr', 'media_final'
        ]
    
    def get_media_final(self, obj):
        """Calcula média final se houver notas"""
        notas = [n for n in [obj.ap1, obj.ap2, obj.cr] if n is not None]
        if notas:
            return sum(notas) / len(notas)
        return None


class PresencaSerializer(serializers.ModelSerializer):
    """Serializer para registro de presenças"""
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    
    class Meta:
        model = Presenca
        fields = [
            'id', 'turma', 'turma_nome', 'aluno', 'aluno_nome',
            'data', 'presente'
        ]


class PresencaListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de presenças"""
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    
    class Meta:
        model = Presenca
        fields = ['id', 'aluno_nome', 'data', 'presente']


# ============================================================================
# SERIALIZERS DE INSCRIÇÕES E DOCUMENTOS
# ============================================================================

class InscricaoSerializer(serializers.ModelSerializer):
    """Serializer completo para inscrições"""
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    aluno_matricula = serializers.CharField(source='aluno.matricula', read_only=True)
    vaga_nome = serializers.CharField(source='vaga.nome', read_only=True)
    total_documentos = serializers.SerializerMethodField()
    
    class Meta:
        model = Inscricao
        fields = [
            'id', 'status', 'data_inscricao',
            'aluno', 'aluno_nome', 'aluno_matricula',
            'vaga', 'vaga_nome', 'total_documentos'
        ]
    
    def get_total_documentos(self, obj):
        return obj.documentos.count()


class InscricaoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de inscrições"""
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    vaga_nome = serializers.CharField(source='vaga.nome', read_only=True)
    
    class Meta:
        model = Inscricao
        fields = [
            'id', 'aluno_nome', 'vaga_nome', 'status', 'data_inscricao'
        ]


class DocumentoSerializer(serializers.ModelSerializer):
    """Serializer para documentos de inscrição"""
    inscricao_info = serializers.SerializerMethodField()
    aluno_nome = serializers.CharField(source='inscricao.aluno.nome', read_only=True)
    
    class Meta:
        model = Documento
        fields = [
            'id', 'inscricao', 'inscricao_info', 'aluno_nome',
            'tipo', 'arquivo', 'nome_arquivo', 'enviado_em', 'observacao'
        ]
    
    def get_inscricao_info(self, obj):
        return f"{obj.inscricao.aluno.nome} - {obj.inscricao.vaga.nome}"


# ============================================================================
# SERIALIZERS DE HORAS E PAGAMENTOS
# ============================================================================

class RegistroHorasSerializer(serializers.ModelSerializer):
    """Serializer completo para registro de horas"""
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    monitor_nome = serializers.CharField(source='monitor.nome', read_only=True)
    validador_nome = serializers.CharField(source='validado_por.nome', read_only=True)
    
    class Meta:
        model = RegistroHoras
        fields = [
            'id', 'turma', 'turma_nome', 'monitor', 'monitor_nome',
            'data', 'hora_inicio', 'hora_fim', 'total_horas',
            'descricao_atividade', 'status', 'validado_por',
            'validador_nome', 'data_validacao', 'observacao_validador',
            'criado_em'
        ]
        read_only_fields = ['total_horas', 'criado_em']


class RegistroHorasListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de horas"""
    monitor_nome = serializers.CharField(source='monitor.nome', read_only=True)
    
    class Meta:
        model = RegistroHoras
        fields = [
            'id', 'monitor_nome', 'data', 'total_horas', 'status'
        ]


class StatusPagamentoSerializer(serializers.ModelSerializer):
    """Serializer completo para status de pagamento"""
    monitor_nome = serializers.CharField(source='monitor.nome', read_only=True)
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    processador_nome = serializers.CharField(source='processado_por.nome', read_only=True)
    
    class Meta:
        model = StatusPagamento
        fields = [
            'id', 'monitor', 'monitor_nome', 'turma', 'turma_nome',
            'mes_referencia', 'valor_total', 'status',
            'processado_por', 'processador_nome', 'data_processamento',
            'observacao', 'criado_em'
        ]
        read_only_fields = ['valor_total', 'criado_em']


class StatusPagamentoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de pagamentos"""
    monitor_nome = serializers.CharField(source='monitor.nome', read_only=True)
    
    class Meta:
        model = StatusPagamento
        fields = [
            'id', 'monitor_nome', 'mes_referencia', 'valor_total', 'status'
        ]


# ============================================================================
# SERIALIZERS DE MATERIAIS
# ============================================================================

class MaterialApoioSerializer(serializers.ModelSerializer):
    """Serializer completo para materiais de apoio"""
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    monitor_nome = serializers.CharField(source='monitor.nome', read_only=True)
    
    class Meta:
        model = MaterialApoio
        fields = [
            'id', 'turma', 'turma_nome', 'monitor', 'monitor_nome',
            'titulo', 'tipo', 'descricao', 'arquivo',
            'criado_em', 'atualizado_em', 'publicado'
        ]


class MaterialApoioListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de materiais"""
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    
    class Meta:
        model = MaterialApoio
        fields = [
            'id', 'titulo', 'tipo', 'turma_nome', 'criado_em', 'publicado'
        ]


# ============================================================================
# SERIALIZERS DE ESTATÍSTICAS
# ============================================================================

class EstatisticasSerializer(serializers.Serializer):
    """Serializer para estatísticas gerais do sistema"""
    total_alunos = serializers.IntegerField()
    total_funcionarios = serializers.IntegerField()
    total_vagas = serializers.IntegerField()
    total_turmas = serializers.IntegerField()
    total_inscricoes = serializers.IntegerField()
    vagas_ativas = serializers.IntegerField()
    turmas_ativas = serializers.IntegerField()
    inscricoes_pendentes = serializers.IntegerField()
    inscricoes_aprovadas = serializers.IntegerField()
    total_presencas = serializers.IntegerField()
    total_materiais = serializers.IntegerField()
