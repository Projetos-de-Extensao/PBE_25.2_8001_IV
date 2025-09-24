from django.db import models

# Create your models here.
from django.db import models




"""Modelos para o sistema de gerenciamento de usuários, cursos, vagas e turmas.

Classes:
    TipoUsuario: Define os tipos de usuários (admin, professor, coordenador, aluno).
    Curso: Representa um curso oferecido na plataforma.
    Usuario: Representa um usuário da plataforma (aluno, professor, etc.).
    Vaga: Representa uma vaga de emprego ou estágio.
    Turma: Representa uma turma de um curso.

"""
class TipoUsuario(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50) # Ex: admin, professor, coordenador e aluno.
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.tipo

class Curso(models.Model):
    id = models.AutoField(primary_key=True)
    curso = models.CharField(max_length=50)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.curso

class Salas(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=50)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.numero


class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    ativo = models.BooleanField(default=True)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Vaga(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    coordenador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='vagas_coordenadas')
    descricao = models.TextField()
    requisitos = models.TextField()
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Inscricao(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pendente')  # Ex: Pendente, Aprovado, Rejeitado

    def __str__(self):
        return f"{self.usuario} - {self.vaga} ({self.status})"


class Turma(models.Model):
    id = models.AutoField(primary_key=True)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    sala = models.ForeignKey(Salas, on_delete=models.CASCADE)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    dias_da_semana = models.CharField(max_length=100)  # Ex: "Segunda, Quarta, Sexta"
    horario = models.CharField(max_length=50)  # Ex: "18:00 - 21:00"
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


