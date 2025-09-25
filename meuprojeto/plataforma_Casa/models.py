from django.db import models

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