╔════════════════════════════════════════════════════════════════════════════════╗
║                   GUIA: ADICIONAR ROLE "MONITOR" A UM ALUNO                     ║
║              Plataforma Casa - Sistema de Monitorias - Django                   ║
╚════════════════════════════════════════════════════════════════════════════════╝

Este guia mostra 3 formas de adicionar o role "Monitor" a um usuário que já é Aluno:

================================================================================
📌 OPÇÃO 1: VIA DJANGO ADMIN (INTERFACE GRÁFICA)
================================================================================

1. ACESSAR ADMIN:
   ─────────────────────────────────────────────────────────────────────────
   http://localhost:8000/admin/
   
   Fazer login com credenciais de admin:
   Username: admin
   Senha: admin

2. LOCALIZAR USUÁRIO:
   ─────────────────────────────────────────────────────────────────────────
   a) No dashboard do admin, clique em "Users" (Usuários)
   b) Procure pelo nome do usuário na lista
   c) Clique para editar

3. ADICIONAR GRUPO "MONITOR":
   ─────────────────────────────────────────────────────────────────────────
   a) Na página de edição do usuário, procure pela seção "Groups"
   b) Na caixa de grupos "Available groups" encontre "Monitor"
   c) Clique em "Monitor" para selecioná-lo
   d) Clique na seta "→" para mover para "Chosen groups"
   e) Clique em "Guardar" (ou "Save")

4. VERIFICAÇÃO:
   ─────────────────────────────────────────────────────────────────────────
   ✓ Deve aparecer "Monitor" em "Chosen groups"
   ✓ O usuário agora tem role de Monitor
   ✓ Mantém também o role de Aluno

================================================================================
📌 OPÇÃO 2: VIA SHELL DO DJANGO
================================================================================

1. ACESSAR SHELL:
   ─────────────────────────────────────────────────────────────────────────
   cd /Users/anderson/my_folders/repositoriolocal/PBE_25.2_8001_IV/meuprojeto
   python manage.py shell

2. EXECUTAR COMANDOS:
   ─────────────────────────────────────────────────────────────────────────
   
   # Importar necessários
   from django.contrib.auth.models import User, Group
   
   # Obter o usuário (substitua por username real)
   user = User.objects.get(username='usuario_teste_cadastro')
   
   # Obter/criar grupo Monitor
   grupo_monitor, _ = Group.objects.get_or_create(name='Monitor')
   
   # Adicionar ao usuário
   user.groups.add(grupo_monitor)
   
   # Verificar
   print(user.groups.all())
   # Saída esperada: <QuerySet [<Group: Aluno>, <Group: Monitor>]>

3. SAÍDA ESPERADA:
   ─────────────────────────────────────────────────────────────────────────
   <QuerySet [<Group: Aluno>, <Group: Monitor>]>

================================================================================
📌 OPÇÃO 3: VIA SCRIPT PYTHON
================================================================================

1. CRIAR ARQUIVO: aprova_monitor.py
   ─────────────────────────────────────────────────────────────────────────
   
   Salve o seguinte código como aprova_monitor.py na pasta /meuprojeto/

"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

from django.contrib.auth.models import User, Group

def aprovar_monitor(username):
    '''Adiciona role Monitor ao usuário'''
    
    print(f"\n🔄 Processando aprovação para Monitor...")
    print(f"   Username: {username}")
    
    try:
        # Obter usuário
        user = User.objects.get(username=username)
        print(f"✅ Usuário encontrado: {user.get_full_name() or user.username}")
        
        # Obter/criar grupo Monitor
        grupo_monitor, criado = Group.objects.get_or_create(name='Monitor')
        if criado:
            print(f"✅ Grupo 'Monitor' criado")
        
        # Verificar se já é monitor
        if user.groups.filter(name='Monitor').exists():
            print(f"ℹ️  Usuário já tem role de Monitor")
            return False
        
        # Adicionar ao grupo
        user.groups.add(grupo_monitor)
        print(f"✅ Role 'Monitor' adicionado com sucesso!")
        
        # Verificar grupos
        grupos = user.groups.all()
        print(f"   Grupos: {', '.join([g.name for g in grupos])}")
        
        return True
    
    except User.DoesNotExist:
        print(f"❌ Usuário não encontrado: {username}")
        return False
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python aprova_monitor.py <username>")
        print("Exemplo: python aprova_monitor.py joao.silva")
        sys.exit(1)
    
    username = sys.argv[1]
    sucesso = aprovar_monitor(username)
    sys.exit(0 if sucesso else 1)
"""

2. EXECUTAR SCRIPT:
   ─────────────────────────────────────────────────────────────────────────
   cd /Users/anderson/my_folders/repositoriolocal/PBE_25.2_8001_IV/meuprojeto
   python aprova_monitor.py usuario_teste_cadastro

3. SAÍDA ESPERADA:
   ─────────────────────────────────────────────────────────────────────────
   🔄 Processando aprovação para Monitor...
      Username: usuario_teste_cadastro
   ✅ Usuário encontrado: Teste Cadastro
   ✅ Grupo 'Monitor' criado
   ✅ Role 'Monitor' adicionado com sucesso!
      Grupos: Aluno, Monitor

================================================================================
🔧 VERIFICAR SE USUÁRIO TEM ROLE MONITOR
================================================================================

VIA SHELL:
─────────────────────────────────────────────────────────────────────────────
from django.contrib.auth.models import User

user = User.objects.get(username='usuario_teste_cadastro')

# Verificar se é aluno
print(user.groups.filter(name='Aluno').exists())  # True

# Verificar se é monitor
print(user.groups.filter(name='Monitor').exists())  # True

# Listar todos os grupos
print(user.groups.all())  # <QuerySet [<Group: Aluno>, <Group: Monitor>]>

VIA ADMIN:
─────────────────────────────────────────────────────────────────────────────
1. Abra http://localhost:8000/admin/auth/user/
2. Clique no usuário
3. Em "Chosen groups" deve aparecer "Aluno" e "Monitor"

================================================================================
📊 FLUXO COMPLETO DE APROVAÇÃO
================================================================================

1. USUÁRIO SE CADASTRA
   └─> Role "Aluno" atribuído automaticamente
   └─> Acessa Portal de Vagas
   └─> Inscreve-se em monitoria

2. PROFESSOR REVISA INSCRIÇÃO
   └─> Aluno é "Aprovado" na inscrição
   └─> Professor deve adicionar role "Monitor"
   └─> Pode usar qualquer método acima

3. USUÁRIO AGORA É MONITOR
   └─> Acessa Dashboard de Monitor
   └─> Pode ministrar turmas
   └─> Pode registrar horas
   └─> Ainda tem acesso à Portal de Vagas (como Aluno)

4. VISUALIZAR DASHBOARD CORRETO
   ├─ Se for apenas Aluno → vai para Portal de Vagas
   ├─ Se for Monitor → vai para Dashboard de Monitor
   └─ Se for Professor/Admin → vai para Dashboard próprio

================================================================================
⚠️  NOTAS IMPORTANTES
================================================================================

✓ Um usuário pode ter MÚLTIPLOS roles simultaneamente
✓ Ter role "Monitor" não remove role "Aluno"
✓ As permissões são controladas pelos Decorators @requer_grupo()
✓ O sistema verifica Groups do usuário, não campo separado
✓ Mudanças são imediatas (sem reiniciar servidor)
✓ Logs são registrados no console

================================================================================
🚀 EXEMPLO PRÁTICO COMPLETO
================================================================================

CENÁRIO: Joanna Silva completou cadastro como Aluna
OBJETIVO: Aprová-la como Monitor

PASSO 1: Joanna se registra em http://localhost:8000/register/
─────────────────────────────────────────────────────────────────────────────
Nome: Joanna Silva
Email: joanna.silva@email.com
Username: joanna.silva
Matrícula: 2024001
Curso: Engenharia de Software
Período: 3º
CR: 8.5
Senha: JoannaSenha@123

✅ Cadastro realizado
✅ Role "Aluno" atribuído automaticamente
✅ Pode fazer login

PASSO 2: Joanna faz login e se inscreve em monitoria
─────────────────────────────────────────────────────────────────────────────
Login com: joanna.silva / JoannaSenha@123
→ Acessa Portal de Vagas
→ Inscreve-se em "Monitoria de Cálculo"
→ Inscrição fica em "Pendente"

PASSO 3: Professor analisa e aprova a inscrição
─────────────────────────────────────────────────────────────────────────────
Professor acessa Dashboard
→ Vê inscrição de Joanna
→ Aprova inscrição

PASSO 4: Admin aprova como Monitor
─────────────────────────────────────────────────────────────────────────────
Método 1 (Admin interface):
   → http://localhost:8000/admin/auth/user/
   → Procura "joanna.silva"
   → Adiciona grupo "Monitor"
   → Salva

Método 2 (Shell):
   python manage.py shell
   from django.contrib.auth.models import User, Group
   user = User.objects.get(username='joanna.silva')
   grupo = Group.objects.get(name='Monitor')
   user.groups.add(grupo)

PASSO 5: Joanna agora tem ambos os roles
─────────────────────────────────────────────────────────────────────────────
✓ Role: Aluno (original)
✓ Role: Monitor (novo)

Próximos acessos:
→ Login com joanna.silva
→ Sistema detecta que é Monitor
→ Redireciona para Dashboard de Monitor
→ Pode ministrar aulas
→ Pode registrar horas

================================================================================
❓ DÚVIDAS FREQUENTES
================================================================================

P: E se o usuário já é Aluno, como adiciono Monitor?
R: Use qualquer um dos 3 métodos acima. Ele manterá o role Aluno
   e receberá o role Monitor (múltiplos roles suportados).

P: Como remover o role Monitor?
R: Via admin, remova "Monitor" da seção "Chosen groups"
   Via shell: user.groups.remove(grupo_monitor)

P: O usuário recebe email quando é aprovado como Monitor?
R: Não, mas você pode implementar isso nas views.

P: Qual é a diferença entre Aluno e Monitor?
R: Aluno: pode se inscrever em vagas
   Monitor: pode ministrar monitorias

P: Um Aluno pode ser Monitor de várias turmas?
R: Sim, não há limite.

P: Se o rol não funcionar, o que fazer?
R: 1. Verifique se o grupo "Monitor" existe no admin
   2. Verifique se o usuário está no grupo (admin/user)
   3. Reinicie o servidor Django
   4. Limpe o cache do navegador

================================================================================
✅ CONCLUSÃO
================================================================================

O sistema de roles está totalmente implementado e pronto!

Qualquer dúvida ou problema, consulte:
- IMPLEMENTACAO_CADASTRO.md (documentação completa)
- teste_registro.py (script de teste)
- http://localhost:8000/admin/ (interface gráfica)
