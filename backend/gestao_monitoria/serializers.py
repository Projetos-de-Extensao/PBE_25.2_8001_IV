from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (AgendamentoMonitoria, AlunoProfile, Curso,
                     FuncionarioProfile, HorarioDisponivel, Inscricao,
                     ParticipacaoMonitoria, Presenca, Sala, SubmissaoHoras,
                     Turma, Vaga)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'


class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = '__all__'


class FuncionarioSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = FuncionarioProfile
        fields = '__all__'


class AlunoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    curso_nome = serializers.CharField(source='curso.nome', read_only=True)
    
    class Meta:
        model = AlunoProfile
        fields = '__all__'


class VagaSerializer(serializers.ModelSerializer):
    curso_nome = serializers.CharField(source='curso.nome', read_only=True)
    coordenador_nome = serializers.CharField(
        source='coordenador.user.get_full_name', read_only=True
    )
    monitores_detalhes = AlunoSerializer(source='monitores', many=True, read_only=True)
    
    class Meta:
        model = Vaga
        fields = '__all__'


class TurmaSerializer(serializers.ModelSerializer):
    vaga_nome = serializers.CharField(source='vaga.nome', read_only=True)
    sala_numero = serializers.CharField(source='sala.numero', read_only=True)
    monitor_nome = serializers.CharField(
        source='monitor.user.get_full_name', read_only=True
    )
    curso_nome = serializers.CharField(source='curso.nome', read_only=True)
    
    class Meta:
        model = Turma
        fields = '__all__'


class ParticipacaoMonitoriaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(
        source='aluno.user.get_full_name', read_only=True
    )
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    
    class Meta:
        model = ParticipacaoMonitoria
        fields = '__all__'


class PresencaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(
        source='aluno.user.get_full_name', read_only=True
    )
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    
    class Meta:
        model = Presenca
        fields = '__all__'


class InscricaoSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(
        source='aluno.user.get_full_name', read_only=True
    )
    vaga_nome = serializers.CharField(source='vaga.nome', read_only=True)
    
    class Meta:
        model = Inscricao
        fields = '__all__'


# Novos serializers para o sistema de monitorias

class HorarioDisponivelSerializer(serializers.ModelSerializer):
    monitor_nome = serializers.CharField(
        source='monitor.user.get_full_name', read_only=True
    )
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    
    class Meta:
        model = HorarioDisponivel
        fields = '__all__'


class AgendamentoMonitoriaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(
        source='aluno.user.get_full_name', read_only=True
    )
    monitor_nome = serializers.CharField(
        source='monitor.user.get_full_name', read_only=True
    )
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    
    class Meta:
        model = AgendamentoMonitoria
        fields = '__all__'


class SubmissaoHorasSerializer(serializers.ModelSerializer):
    monitor_nome = serializers.CharField(
        source='monitor.user.get_full_name', read_only=True
    )
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    aprovado_por_nome = serializers.CharField(
        source='aprovado_por.user.get_full_name', read_only=True, allow_null=True
    )
    
    class Meta:
        model = SubmissaoHoras
        fields = '__all__'


# Serializers para autenticação

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

