from django.contrib import admin
from .models import TipoUsuario, Curso, Salas, Usuario, Vaga, Inscricao
    
# Register your models here.
admin.site.register(TipoUsuario)
admin.site.register(Curso)
admin.site.register(Salas)
admin.site.register(Usuario)
admin.site.register(Vaga)
admin.site.register(Inscricao)
