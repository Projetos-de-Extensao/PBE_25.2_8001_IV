from django.contrib import admin
from django.contrib.auth.models import User

from .models import (AgendamentoMonitoria, AlunoProfile, Curso,
                     FuncionarioProfile, HorarioDisponivel, Inscricao,
                     ParticipacaoMonitoria, Presenca, Sala, SubmissaoHoras,
                     Turma, TurmaDiaSemana, Vaga)

# Register your models here.
admin.site.register(Curso)
admin.site.register(Sala)
admin.site.register(FuncionarioProfile)
admin.site.register(AlunoProfile)
admin.site.register(Vaga)
admin.site.register(Turma)
admin.site.register(TurmaDiaSemana)
admin.site.register(Inscricao)
admin.site.register(ParticipacaoMonitoria)
admin.site.register(Presenca)
admin.site.register(HorarioDisponivel)
admin.site.register(AgendamentoMonitoria)
admin.site.register(SubmissaoHoras)












