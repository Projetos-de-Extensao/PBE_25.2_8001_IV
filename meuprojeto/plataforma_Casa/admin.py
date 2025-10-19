from django.contrib import admin
from .models import (
    Usuario, Funcionario, Aluno, Vaga, Turma, Inscricao, Curso, 
    TipoUsuario, Sala, ParticipacaoMonitoria, Presenca,
    Documento, RegistroHoras, StatusPagamento
)

# Register your models here.

# Customizar StatusPagamento para mostrar apenas pagamentos de semestre
class StatusPagamentoAdmin(admin.ModelAdmin):
    list_display = ('monitor', 'turma', 'mes_referencia', 'valor_total', 'status')
    list_filter = ('status', 'mes_referencia')
    search_fields = ('monitor__nome', 'turma__nome')
    readonly_fields = ('valor_total',)
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('monitor', 'turma', 'mes_referencia')
        }),
        ('Valor do Semestre', {
            'fields': ('valor_total',),
            'description': 'Valor fixo de R$ 1.500,00 por semestre'
        }),
        ('Status e Processamento', {
            'fields': ('status', 'processado_por', 'data_processamento')
        }),
        ('Observações', {
            'fields': ('observacao',)
        }),
    )

admin.site.register(TipoUsuario)
admin.site.register(Curso)
admin.site.register(Usuario)
admin.site.register(Funcionario)
admin.site.register(Aluno)
admin.site.register(Vaga)
admin.site.register(Inscricao)
admin.site.register(Turma)
admin.site.register(Sala)
admin.site.register(Presenca)
admin.site.register(ParticipacaoMonitoria)
admin.site.register(Documento)
admin.site.register(RegistroHoras)
admin.site.register(StatusPagamento, StatusPagamentoAdmin)












