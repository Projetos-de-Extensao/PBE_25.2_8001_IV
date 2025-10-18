"""
Modelos refatorados para o Sistema de Gestão de Monitorias (SGM) Ibmec
"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# ========================
# MODELOS BASE ABSTRATOS
# ========================

class TimeStampedModel(models.Model):
    """Modelo abstrato com timestamps de criação e atualização"""
    created_at = models.DateTimeField(
        _('criado em'),
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        _('atualizado em'),
        auto_now=True,
        editable=False
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']


class ActiveModel(models.Model):
    """Modelo abstrato com soft delete via campo ativo"""
    ativo = models.BooleanField(_('ativo'), default=True, db_index=True)

    class Meta:
        abstract = True

    def desativar(self):
        """Soft delete do registro"""
        self.ativo = False
        self.save(update_fields=['ativo'])

    def ativar(self):
        """Reativa um registro desativado"""
        self.ativo = True
        self.save(update_fields=['ativo'])


class BaseModel(TimeStampedModel, ActiveModel):
    """Modelo base completo com timestamps e soft delete"""
    class Meta:
        abstract = True


# ========================
# CHOICES/ENUMS
# ========================

class DiaSemana(models.IntegerChoices):
    """Dias da semana como IntegerChoices para queries eficientes"""
    SEGUNDA = 0, _('Segunda-feira')
    TERCA = 1, _('Terça-feira')
    QUARTA = 2, _('Quarta-feira')
    QUINTA = 3, _('Quinta-feira')
    SEXTA = 4, _('Sexta-feira')
    SABADO = 5, _('Sábado')
    DOMINGO = 6, _('Domingo')


class StatusInscricao(models.TextChoices):
    """Status possíveis para inscrições em vagas"""
    PENDENTE = 'pendente', _('Pendente')
    APROVADO = 'aprovado', _('Aprovado')
    REJEITADO = 'rejeitado', _('Rejeitado')


class StatusAgendamento(models.TextChoices):
    """Status possíveis para agendamentos de monitoria"""
    PENDENTE = 'pendente', _('Pendente')
    CONFIRMADO = 'confirmado', _('Confirmado')
    CANCELADO = 'cancelado', _('Cancelado')
    CONCLUIDO = 'concluido', _('Concluído')


class StatusSubmissao(models.TextChoices):
    """Status possíveis para submissão de horas"""
    PENDENTE = 'pendente', _('Pendente')
    APROVADO = 'aprovado', _('Aprovado')
    REJEITADO = 'rejeitado', _('Rejeitado')


# ========================
# MODELOS ACADÊMICOS
# ========================

class Curso(BaseModel):
    """Cursos oferecidos pela instituição"""
    nome = models.CharField(_('nome'), max_length=100, unique=True)
    codigo = models.CharField(_('código'), max_length=20, unique=True, blank=True)
    descricao = models.TextField(_('descrição'), blank=True)

    class Meta:
        verbose_name = _('curso')
        verbose_name_plural = _('cursos')
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Sala(BaseModel):
    """Salas disponíveis para monitorias"""
    numero = models.CharField(_('número'), max_length=20, unique=True)
    bloco = models.CharField(_('bloco'), max_length=10, blank=True)
    capacidade = models.PositiveIntegerField(
        _('capacidade'),
        null=True,
        blank=True,
        validators=[MinValueValidator(1)]
    )
    observacoes = models.TextField(_('observações'), blank=True)

    class Meta:
        verbose_name = _('sala')
        verbose_name_plural = _('salas')
        ordering = ['numero']
        indexes = [
            models.Index(fields=['numero', 'ativo']),
        ]

    def __str__(self):
        if self.bloco:
            return f"Sala {self.numero} - Bloco {self.bloco}"
        return f"Sala {self.numero}"


# ========================
# PERFIS DE USUÁRIOS
# ========================

class FuncionarioProfile(BaseModel):
    """Perfil de funcionário vinculado ao User do Django"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='funcionario',
        verbose_name=_('usuário')
    )
    matricula = models.CharField(
        _('matrícula'),
        max_length=20,
        unique=True,
        db_index=True
    )
    departamento = models.CharField(
        _('departamento'),
        max_length=100,
        blank=True
    )
    coordenador = models.BooleanField(_('é coordenador'), default=False)
    telefone = models.CharField(_('telefone'), max_length=20, blank=True)

    class Meta:
        verbose_name = _('funcionário')
        verbose_name_plural = _('funcionários')
        ordering = ['user__first_name', 'user__last_name']

    def __str__(self):
        nome = self.user.get_full_name() or self.user.username
        return f"{nome} - {self.matricula}"

    @property
    def nome_completo(self):
        return self.user.get_full_name() or self.user.username


class AlunoProfile(BaseModel):
    """Perfil de aluno vinculado ao User do Django"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='aluno',
        verbose_name=_('usuário')
    )
    matricula = models.CharField(
        _('matrícula'),
        max_length=20,
        unique=True,
        db_index=True
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.PROTECT,
        related_name='alunos',
        verbose_name=_('curso')
    )
    data_ingresso = models.DateField(_('data de ingresso'))
    periodo = models.PositiveIntegerField(
        _('período'),
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    cr_geral = models.DecimalField(
        _('CR geral'),
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        blank=True
    )
    telefone = models.CharField(_('telefone'), max_length=20, blank=True)

    class Meta:
        verbose_name = _('aluno')
        verbose_name_plural = _('alunos')
        ordering = ['user__first_name', 'user__last_name']
        indexes = [
            models.Index(fields=['matricula', 'ativo']),
            models.Index(fields=['curso', 'periodo']),
        ]

    def __str__(self):
        nome = self.user.get_full_name() or self.user.username
        return f"{nome} - {self.matricula}"

    @property
    def nome_completo(self):
        return self.user.get_full_name() or self.user.username

    def clean(self):
        """Validações customizadas"""
        super().clean()
        if self.data_ingresso and self.data_ingresso > timezone.now().date():
            raise ValidationError({
                'data_ingresso': _('Data de ingresso não pode ser futura.')
            })


# Aliases para compatibilidade com código existente
Aluno = AlunoProfile
Funcionario = FuncionarioProfile


# ========================
# SISTEMA DE VAGAS E TURMAS
# ========================

class Vaga(BaseModel):
    """Vagas de monitoria disponíveis"""
    nome = models.CharField(_('nome'), max_length=150)
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='vagas',
        verbose_name=_('curso')
    )
    coordenador = models.ForeignKey(
        FuncionarioProfile,
        on_delete=models.PROTECT,
        related_name='vagas_coordenadas',
        verbose_name=_('coordenador')
    )
    descricao = models.TextField(_('descrição'))
    requisitos = models.TextField(_('requisitos'))
    vagas_disponiveis = models.PositiveIntegerField(
        _('vagas disponíveis'),
        default=1,
        validators=[MinValueValidator(1)]
    )
    monitores = models.ManyToManyField(
        AlunoProfile,
        through='Inscricao',
        related_name='vagas_monitoria',
        verbose_name=_('monitores'),
        blank=True
    )

    class Meta:
        verbose_name = _('vaga de monitoria')
        verbose_name_plural = _('vagas de monitoria')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['curso', 'ativo']),
            models.Index(fields=['coordenador', 'ativo']),
        ]

    def __str__(self):
        return f"{self.nome} - {self.curso}"

    @property
    def vagas_preenchidas(self):
        """Retorna quantidade de vagas já preenchidas"""
        return self.inscricoes.filter(status=StatusInscricao.APROVADO).count()

    @property
    def tem_vagas(self):
        """Verifica se ainda há vagas disponíveis"""
        return self.vagas_preenchidas < self.vagas_disponiveis


class Turma(BaseModel):
    """Turmas de monitoria em execução"""
    nome = models.CharField(_('nome'), max_length=150)
    vaga = models.ForeignKey(
        Vaga,
        on_delete=models.CASCADE,
        related_name='turmas',
        verbose_name=_('vaga')
    )
    sala = models.ForeignKey(
        Sala,
        on_delete=models.PROTECT,
        related_name='turmas',
        verbose_name=_('sala')
    )
    descricao = models.TextField(_('descrição'), blank=True)
    data_inicio = models.DateField(_('data de início'))
    data_fim = models.DateField(_('data de término'))
    
    # Horários estruturados (substituindo strings)
    hora_inicio = models.TimeField(_('hora de início'))
    hora_fim = models.TimeField(_('hora de término'))
    
    monitor = models.ForeignKey(
        AlunoProfile,
        on_delete=models.PROTECT,
        related_name='turmas_monitoria',
        verbose_name=_('monitor')
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='turmas',
        verbose_name=_('curso')
    )

    class Meta:
        verbose_name = _('turma de monitoria')
        verbose_name_plural = _('turmas de monitoria')
        ordering = ['-data_inicio']
        indexes = [
            models.Index(fields=['curso', 'ativo']),
            models.Index(fields=['monitor', 'ativo']),
            models.Index(fields=['data_inicio', 'data_fim']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(data_fim__gte=models.F('data_inicio')),
                name='turma_data_fim_valida'
            ),
            models.CheckConstraint(
                check=models.Q(hora_fim__gt=models.F('hora_inicio')),
                name='turma_hora_fim_valida'
            ),
        ]

    def __str__(self):
        return f"{self.nome} - {self.monitor}"

    def clean(self):
        """Validações customizadas"""
        super().clean()
        if self.data_fim and self.data_inicio and self.data_fim < self.data_inicio:
            raise ValidationError({
                'data_fim': _('Data de término deve ser posterior à data de início.')
            })
        if self.hora_fim and self.hora_inicio and self.hora_fim <= self.hora_inicio:
            raise ValidationError({
                'hora_fim': _('Hora de término deve ser posterior à hora de início.')
            })


class TurmaDiaSemana(models.Model):
    """Relacionamento M2M entre Turma e dias da semana"""
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name='dias_semana'
    )
    dia = models.IntegerField(
        _('dia da semana'),
        choices=DiaSemana.choices
    )

    class Meta:
        verbose_name = _('dia da semana da turma')
        verbose_name_plural = _('dias da semana das turmas')
        unique_together = [['turma', 'dia']]
        ordering = ['dia']

    def __str__(self):
        return f"{self.turma.nome} - {self.get_dia_display()}"


# ========================
# PARTICIPAÇÃO E PRESENÇA
# ========================

class ParticipacaoMonitoria(TimeStampedModel):
    """Registro de participação e notas de alunos em monitorias"""
    aluno = models.ForeignKey(
        AlunoProfile,
        on_delete=models.CASCADE,
        related_name='participacoes',
        verbose_name=_('aluno')
    )
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name='participacoes',
        verbose_name=_('turma')
    )
    ap1 = models.DecimalField(
        _('AP1'),
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    ap2 = models.DecimalField(
        _('AP2'),
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    cr = models.DecimalField(
        _('CR'),
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    observacoes = models.TextField(_('observações'), blank=True)

    class Meta:
        verbose_name = _('participação em monitoria')
        verbose_name_plural = _('participações em monitorias')
        unique_together = [['aluno', 'turma']]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.aluno} - {self.turma}"


class Presenca(TimeStampedModel):
    """Registro de presença em aulas de monitoria"""
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name='presencas',
        verbose_name=_('turma')
    )
    aluno = models.ForeignKey(
        AlunoProfile,
        on_delete=models.CASCADE,
        related_name='presencas',
        verbose_name=_('aluno')
    )
    data = models.DateField(_('data'))
    presente = models.BooleanField(_('presente'), default=False)
    observacoes = models.TextField(_('observações'), blank=True)

    class Meta:
        verbose_name = _('presença')
        verbose_name_plural = _('presenças')
        unique_together = [['turma', 'aluno', 'data']]
        ordering = ['-data']
        indexes = [
            models.Index(fields=['turma', 'data']),
            models.Index(fields=['aluno', 'data']),
        ]

    def __str__(self):
        status = 'Presente' if self.presente else 'Ausente'
        return f"{self.aluno} - {self.turma} ({self.data}) - {status}"


class Inscricao(TimeStampedModel):
    """Inscrições de alunos em vagas de monitoria"""
    aluno = models.ForeignKey(
        AlunoProfile,
        on_delete=models.CASCADE,
        related_name='inscricoes',
        verbose_name=_('aluno')
    )
    vaga = models.ForeignKey(
        Vaga,
        on_delete=models.CASCADE,
        related_name='inscricoes',
        verbose_name=_('vaga')
    )
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=StatusInscricao.choices,
        default=StatusInscricao.PENDENTE,
        db_index=True
    )
    justificativa = models.TextField(_('justificativa'), blank=True)
    avaliado_por = models.ForeignKey(
        FuncionarioProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inscricoes_avaliadas',
        verbose_name=_('avaliado por')
    )
    data_avaliacao = models.DateTimeField(
        _('data de avaliação'),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('inscrição')
        verbose_name_plural = _('inscrições')
        unique_together = [['aluno', 'vaga']]
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['vaga', 'status']),
        ]

    def __str__(self):
        return f"{self.aluno} - {self.vaga} ({self.get_status_display()})"

    def aprovar(self, avaliador):
        """Aprova a inscrição"""
        self.status = StatusInscricao.APROVADO
        self.avaliado_por = avaliador
        self.data_avaliacao = timezone.now()
        self.save()

    def rejeitar(self, avaliador, justificativa=''):
        """Rejeita a inscrição"""
        self.status = StatusInscricao.REJEITADO
        self.justificativa = justificativa
        self.avaliado_por = avaliador
        self.data_avaliacao = timezone.now()
        self.save()


# ========================
# AGENDAMENTOS
# ========================

class HorarioDisponivel(BaseModel):
    """Horários disponíveis dos monitores para agendamento"""
    monitor = models.ForeignKey(
        AlunoProfile,
        on_delete=models.CASCADE,
        related_name='horarios_disponiveis',
        verbose_name=_('monitor')
    )
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name='horarios',
        verbose_name=_('turma')
    )
    dia_semana = models.IntegerField(
        _('dia da semana'),
        choices=DiaSemana.choices
    )
    horario_inicio = models.TimeField(_('horário de início'))
    horario_fim = models.TimeField(_('horário de término'))

    class Meta:
        verbose_name = _('horário disponível')
        verbose_name_plural = _('horários disponíveis')
        ordering = ['dia_semana', 'horario_inicio']
        constraints = [
            models.CheckConstraint(
                check=models.Q(horario_fim__gt=models.F('horario_inicio')),
                name='horario_disponivel_valido'
            ),
        ]

    def __str__(self):
        return (f"{self.monitor} - {self.get_dia_semana_display()} "
                f"{self.horario_inicio}-{self.horario_fim}")


class AgendamentoMonitoria(TimeStampedModel):
    """Agendamentos de monitorias individuais"""
    aluno = models.ForeignKey(
        AlunoProfile,
        on_delete=models.CASCADE,
        related_name='agendamentos',
        verbose_name=_('aluno')
    )
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name='agendamentos',
        verbose_name=_('turma')
    )
    monitor = models.ForeignKey(
        AlunoProfile,
        on_delete=models.PROTECT,
        related_name='monitorias_agendadas',
        verbose_name=_('monitor')
    )
    data = models.DateField(_('data'))
    horario_inicio = models.TimeField(_('horário de início'))
    horario_fim = models.TimeField(_('horário de término'))
    assunto = models.CharField(_('assunto'), max_length=200)
    descricao = models.TextField(_('descrição'), blank=True)
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=StatusAgendamento.choices,
        default=StatusAgendamento.PENDENTE,
        db_index=True
    )

    class Meta:
        verbose_name = _('agendamento de monitoria')
        verbose_name_plural = _('agendamentos de monitoria')
        ordering = ['-data', '-horario_inicio']
        indexes = [
            models.Index(fields=['monitor', 'data']),
            models.Index(fields=['aluno', 'data']),
            models.Index(fields=['status', 'data']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(horario_fim__gt=models.F('horario_inicio')),
                name='agendamento_horario_valido'
            ),
        ]

    def __str__(self):
        return f"{self.aluno} - {self.monitor} ({self.data} {self.horario_inicio})"

    def clean(self):
        """Validações customizadas"""
        super().clean()
        if self.data and self.data < timezone.now().date():
            raise ValidationError({
                'data': _('Não é possível agendar para datas passadas.')
            })


# ========================
# SUBMISSÃO DE HORAS
# ========================

class SubmissaoHoras(TimeStampedModel):
    """Submissão de horas trabalhadas pelos monitores"""
    monitor = models.ForeignKey(
        AlunoProfile,
        on_delete=models.CASCADE,
        related_name='submissoes_horas',
        verbose_name=_('monitor')
    )
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name='submissoes_horas',
        verbose_name=_('turma')
    )
    mes_referencia = models.DateField(_('mês de referência'))
    total_horas = models.DecimalField(
        _('total de horas'),
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    descricao_atividades = models.TextField(_('descrição das atividades'))
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=StatusSubmissao.choices,
        default=StatusSubmissao.PENDENTE,
        db_index=True
    )
    aprovado_por = models.ForeignKey(
        FuncionarioProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='aprovacoes_horas',
        verbose_name=_('aprovado por')
    )
    data_aprovacao = models.DateTimeField(
        _('data de aprovação'),
        null=True,
        blank=True
    )
    observacoes = models.TextField(_('observações'), blank=True)

    class Meta:
        verbose_name = _('submissão de horas')
        verbose_name_plural = _('submissões de horas')
        unique_together = [['monitor', 'turma', 'mes_referencia']]
        ordering = ['-mes_referencia']
        indexes = [
            models.Index(fields=['status', 'mes_referencia']),
            models.Index(fields=['monitor', 'mes_referencia']),
        ]

    def __str__(self):
        return (f"{self.monitor} - {self.mes_referencia.strftime('%m/%Y')} "
                f"- {self.total_horas}h")

    def aprovar(self, aprovador):
        """Aprova a submissão de horas"""
        self.status = StatusSubmissao.APROVADO
        self.aprovado_por = aprovador
        self.data_aprovacao = timezone.now()
        self.save()

    def rejeitar(self, aprovador, observacoes=''):
        """Rejeita a submissão de horas"""
        self.status = StatusSubmissao.REJEITADO
        self.aprovado_por = aprovador
        self.data_aprovacao = timezone.now()
        if observacoes:
            self.observacoes = observacoes
        self.save()
