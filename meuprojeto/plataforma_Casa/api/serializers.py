from rest_framework import serializers

from ..models import Curso, Vaga, Turma, Aluno, Inscricao


class CursoSerializer(serializers.ModelSerializer):
    """Serializa cursos para consumo rápido via Swagger/DRF."""

    class Meta:
        model = Curso
        fields = ['id', 'nome', 'ativo']


class AlunoSerializer(serializers.ModelSerializer):
    # Campo auxiliar somente leitura exibindo o nome do curso vinculado
    curso_nome = serializers.CharField(source='curso.nome', read_only=True)

    class Meta:
        model = Aluno
        fields = [
            'id',
            'nome',
            'email',
            'matricula',
            'curso',
            'curso_nome',
            'periodo',
            'cr_geral',
            'ativo',
        ]


class VagaSerializer(serializers.ModelSerializer):
    # Exibe dados relacionados para facilitar leitura no Swagger
    curso_nome = serializers.CharField(source='curso.nome', read_only=True)
    coordenador_nome = serializers.CharField(source='coordenador.nome', read_only=True)
    vagas_disponiveis = serializers.IntegerField(read_only=True)

    class Meta:
        model = Vaga
        fields = [
            'id',
            'nome',
            'descricao',
            'requisitos',
            'responsabilidades',
            'numero_vagas',
            'disciplina',
            'ativo',
            'criado_em',
            'curso',
            'curso_nome',
            'coordenador',
            'coordenador_nome',
            'vagas_disponiveis',
        ]


class TurmaSerializer(serializers.ModelSerializer):
    # Informações complementares da vaga, sala e monitor (somente leitura)
    vaga_nome = serializers.CharField(source='vaga.nome', read_only=True)
    sala_numero = serializers.CharField(source='sala.numero', read_only=True)
    monitor_nome = serializers.CharField(source='monitor.nome', read_only=True)

    class Meta:
        model = Turma
        fields = [
            'id',
            'nome',
            'descricao',
            'data_inicio',
            'data_fim',
            'dias_da_semana',
            'horario',
            'ativo',
            'criado_em',
            'vaga',
            'vaga_nome',
            'sala',
            'sala_numero',
            'monitor',
            'monitor_nome',
            'curso',
        ]


class InscricaoSerializer(serializers.ModelSerializer):
    # Nome do aluno e da vaga para evitar fazer chamadas extras no front
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    vaga_nome = serializers.CharField(source='vaga.nome', read_only=True)

    class Meta:
        model = Inscricao
        fields = [
            'id',
            'status',
            'data_inscricao',
            'aluno',
            'aluno_nome',
            'vaga',
            'vaga_nome',
        ]
