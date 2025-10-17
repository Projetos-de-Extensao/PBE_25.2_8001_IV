from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class TipoUsuario(models.Model):
    tipo = models.CharField(max_length=50)  # Ex: admin, professor, coordenador, aluno(ideal é ser por código(id))
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.tipo

class Curso(models.Model):
    nome = models.CharField(max_length=50)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Sala(models.Model):
    numero = models.CharField(max_length=50)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.numero

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Funcionario(Usuario):
    matricula = models.CharField(max_length=20, unique=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    coordenador = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} (Funcionário)"

class Aluno(Usuario):
    matricula = models.CharField(max_length=20, unique=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    data_ingresso = models.DateField()
    periodo = models.IntegerField()
    cr_geral = models.FloatField()

    def __str__(self):
        return f"{self.nome} (Aluno)"

class Vaga(models.Model):
    nome = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    coordenador = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='vagas_coordenadas')
    descricao = models.TextField()
    requisitos = models.TextField()
    monitores = models.ManyToManyField(Aluno, related_name='vagas_inscritas', blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    dias_da_semana = models.CharField(max_length=100)  # Ex: "Segunda, Quarta, Sexta"
    horario = models.CharField(max_length=50)  # Ex: "18:00 - 21:00"
    monitor = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='monitorias')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class ParticipacaoMonitoria(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    ap1 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) 
    ap2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    cr = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.aluno} - {self.turma} - ( AP1: {self.ap1}, AP2: {self.ap2}, CR: {self.cr})"

class Presenca(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data = models.DateField()
    presente = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.aluno} - {self.turma} ({self.data}) - {'Presente' if self.presente else 'Ausente'}"

class Inscricao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pendente')  # Ex: Pendente, Aprovado, Rejeitado

    def __str__(self):
        return f"{self.aluno} - {self.vaga} ({self.status})"

class HorarioDisponivel(models.Model):
    """Horários disponíveis dos monitores para agendamento"""
    monitor = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='horarios_disponiveis')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.CharField(max_length=20)  # Segunda, Terça, etc
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.monitor} - {self.dia_semana} {self.horario_inicio}-{self.horario_fim}"

class AgendamentoMonitoria(models.Model):
    """Sistema de agendamento de monitorias pelos alunos"""
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('concluido', 'Concluído'),
    ]
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='agendamentos')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='agendamentos')
    monitor = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='monitorias_agendadas')
    data = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    assunto = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.aluno} - {self.monitor} ({self.data} {self.horario_inicio})"

class SubmissaoHoras(models.Model):
    """Submissão automática de horas pelos monitores"""
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    ]
    
    monitor = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='submissoes_horas')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    mes_referencia = models.DateField()
    total_horas = models.DecimalField(max_digits=5, decimal_places=2)
    descricao_atividades = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    aprovado_por = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True, related_name='aprovacoes')
    data_submissao = models.DateTimeField(auto_now_add=True)
    data_aprovacao = models.DateTimeField(null=True, blank=True)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.monitor} - {self.mes_referencia.strftime('%m/%Y')} - {self.total_horas}h"

# class CustomUser(AbstractUser):
#     """Modelo customizado de usuário para autenticação"""
#     tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.SET_NULL, null=True, blank=True)
#     aluno_profile = models.OneToOneField(Aluno, on_delete=models.CASCADE, null=True, blank=True, related_name='user')
#     funcionario_profile = models.OneToOneField(Funcionario, on_delete=models.CASCADE, null=True, blank=True, related_name='user')
    
#     def __str__(self):
#         return self.username