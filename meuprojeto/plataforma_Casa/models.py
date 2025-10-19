from django.db import models
from decimal import Decimal

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
    responsabilidades = models.TextField(blank=True, null=True)  # Novo campo
    numero_vagas = models.IntegerField(default=1)  # Novo campo
    disciplina = models.CharField(max_length=100, blank=True, null=True)  # Novo campo
    monitores = models.ManyToManyField(Aluno, related_name='vagas_inscritas', blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    
    def vagas_disponiveis(self):
        """Retorna o número de vagas ainda disponíveis"""
        inscritos_aprovados = self.inscricao_set.filter(status='Aprovado').count()
        return max(0, self.numero_vagas - inscritos_aprovados)

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
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Entrevista', 'Entrevista'),
        ('Aprovado', 'Aprovado'),
        ('Não Aprovado', 'Não Aprovado'),
    ]
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pendente')

    def __str__(self):
        return f"{self.aluno} - {self.vaga} ({self.status})"


class Documento(models.Model):
    """Modelo para armazenar documentos dos candidatos"""
    TIPO_CHOICES = [
        ('Histórico Escolar', 'Histórico Escolar'),
        ('Currículo', 'Currículo'),
        ('Carta de Motivação', 'Carta de Motivação'),
        ('Outro', 'Outro'),
    ]
    
    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE, related_name='documentos')
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    arquivo = models.FileField(upload_to='documentos/%Y/%m/%d/')
    nome_arquivo = models.CharField(max_length=255)
    enviado_em = models.DateTimeField(auto_now_add=True)
    observacao = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.tipo} - {self.inscricao.aluno.nome}"


class RegistroHoras(models.Model):
    """Modelo para registro de horas trabalhadas pelos monitores"""
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Aprovado', 'Aprovado'),
        ('Rejeitado', 'Rejeitado'),
    ]
    
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='registros_horas')
    monitor = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='horas_registradas')
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    total_horas = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    descricao_atividade = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pendente')
    validado_por = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True, related_name='horas_validadas')
    data_validacao = models.DateTimeField(null=True, blank=True)
    observacao_validador = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        """Calcula automaticamente o total de horas"""
        from datetime import datetime, timedelta
        inicio = datetime.combine(self.data, self.hora_inicio)
        fim = datetime.combine(self.data, self.hora_fim)
        diferenca = fim - inicio
        self.total_horas = diferenca.total_seconds() / 3600  # Converte para horas
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.monitor} - {self.data} ({self.total_horas}h)"
    
    class Meta:
        verbose_name = 'Registro de Horas'
        verbose_name_plural = 'Registros de Horas'
        ordering = ['-data', '-hora_inicio']


class StatusPagamento(models.Model):
    """Modelo para controle de pagamentos dos monitores - VALOR FIXO DE R$1.500 POR SEMESTRE"""
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Processando', 'Processando'),
        ('Pago', 'Pago'),
        ('Cancelado', 'Cancelado'),
    ]
    
    VALOR_SEMESTRE = Decimal('1500.00')  # Valor fixo: R$1.500 por semestre
    
    monitor = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='pagamentos')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='pagamentos')
    mes_referencia = models.DateField(help_text="Data final do semestre para este pagamento")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=Decimal('1500.00'))
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pendente')
    processado_por = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True, related_name='pagamentos_processados')
    data_processamento = models.DateTimeField(null=True, blank=True)
    observacao = models.TextField(blank=True, null=True, help_text="Observações sobre o pagamento")
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        """Sempre define valor_total como R$1.500 por semestre"""
        self.valor_total = self.VALOR_SEMESTRE
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.monitor} - {self.mes_referencia.strftime('%m/%Y')} - R$ {self.valor_total}"
    
    class Meta:
        verbose_name = 'Status de Pagamento'
        verbose_name_plural = 'Status de Pagamentos'
        ordering = ['-mes_referencia']
