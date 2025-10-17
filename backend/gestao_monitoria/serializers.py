from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    TipoUsuario, Curso, Sala, Usuario, Funcionario, Aluno,
    Vaga, Turma, ParticipacaoMonitoria, Presenca, Inscricao,
    HorarioDisponivel, AgendamentoMonitoria, SubmissaoHoras
)

User = get_user_model()


class TipoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoUsuario
        fields = '__all__'


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'


class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    tipo_usuario_nome = serializers.CharField(source='tipo_usuario.tipo', read_only=True)
    
    class Meta:
        model = Usuario
        fields = '__all__'


class FuncionarioSerializer(serializers.ModelSerializer):
    tipo_usuario_nome = serializers.CharField(source='tipo_usuario.tipo', read_only=True)
    
    class Meta:
        model = Funcionario
        fields = '__all__'


class AlunoSerializer(serializers.ModelSerializer):
    tipo_usuario_nome = serializers.CharField(source='tipo_usuario.tipo', read_only=True)
    curso_nome = serializers.CharField(source='curso.nome', read_only=True)
    
    class Meta:
        model = Aluno
        fields = '__all__'


class VagaSerializer(serializers.ModelSerializer):
    curso_nome = serializers.CharField(source='curso.nome', read_only=True)
    coordenador_nome = serializers.CharField(source='coordenador.nome', read_only=True)
    monitores_detalhes = AlunoSerializer(source='monitores', many=True, read_only=True)
    
    class Meta:
        model = Vaga
        fields = '__all__'


class TurmaSerializer(serializers.ModelSerializer):
    vaga_nome = serializers.CharField(source='vaga.nome', read_only=True)
    sala_numero = serializers.CharField(source='sala.numero', read_only=True)
    monitor_nome = serializers.CharField(source='monitor.nome', read_only=True)
    curso_nome = serializers.CharField(source='curso.nome', read_only=True)
    
    class Meta:
        model = Turma
        fields = '__all__'


class ParticipacaoMonitoriaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    
    class Meta:
        model = ParticipacaoMonitoria
        fields = '__all__'


class PresencaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    
    class Meta:
        model = Presenca
        fields = '__all__'


class InscricaoSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    vaga_nome = serializers.CharField(source='vaga.nome', read_only=True)
    
    class Meta:
        model = Inscricao
        fields = '__all__'

# Novos serializers para o sistema de monitorias

class HorarioDisponivelSerializer(serializers.ModelSerializer):
    monitor_nome = serializers.CharField(source='monitor.nome', read_only=True)
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    
    class Meta:
        model = HorarioDisponivel
        fields = '__all__'

class AgendamentoMonitoriaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    monitor_nome = serializers.CharField(source='monitor.nome', read_only=True)
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    
    class Meta:
        model = AgendamentoMonitoria
        fields = '__all__'

class SubmissaoHorasSerializer(serializers.ModelSerializer):
    monitor_nome = serializers.CharField(source='monitor.nome', read_only=True)
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    aprovado_por_nome = serializers.CharField(source='aprovado_por.nome', read_only=True, allow_null=True)
    
    class Meta:
        model = SubmissaoHoras
        fields = '__all__'

# Serializers para autenticação

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
