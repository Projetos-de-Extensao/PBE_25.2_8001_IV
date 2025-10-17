from django.contrib import admin
from .models import (
    Usuario, Funcionario, Aluno, Vaga, Turma, Inscricao, 
    Curso, TipoUsuario, Sala, ParticipacaoMonitoria, Presenca,
    HorarioDisponivel, AgendamentoMonitoria, SubmissaoHoras
)

# Register your models here.
admin.site.register(TipoUsuario)
admin.site.register(Curso)
admin.site.register(Sala)
admin.site.register(Usuario)
admin.site.register(Funcionario)
admin.site.register(Aluno)
admin.site.register(Vaga)
admin.site.register(Turma)
admin.site.register(Inscricao)
admin.site.register(ParticipacaoMonitoria)
admin.site.register(Presenca)
admin.site.register(HorarioDisponivel)
admin.site.register(AgendamentoMonitoria)
admin.site.register(SubmissaoHoras)












