"""
================================================================================
SCRIPT DE CRIAÇÃO DE USUÁRIOS DE TESTE
================================================================================

Este script cria usuários de teste no sistema com diferentes roles (groups):
- Aluno
- Monitor
- Professor
- Admin

Uso no Heroku:
    heroku run "python meuprojeto/manage.py shell < criar_usuarios_teste.py"

================================================================================
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

# Dados dos usuários de teste
usuarios_teste = [
    {
        'username': 'aluno.teste',
        'email': 'aluno.teste@plataformacasa.com',
        'password': 'aluno123',
        'first_name': 'Aluno',
        'last_name': 'Teste',
        'group': 'Aluno',
        'is_staff': False,
        'is_superuser': False
    },
    {
        'username': 'monitor.teste',
        'email': 'monitor.teste@plataformacasa.com',
        'password': 'monitor123',
        'first_name': 'Monitor',
        'last_name': 'Teste',
        'group': 'Monitor',
        'is_staff': False,
        'is_superuser': False
    },
    {
        'username': 'professor.teste',
        'email': 'professor.teste@plataformacasa.com',
        'password': 'professor123',
        'first_name': 'Professor',
        'last_name': 'Teste',
        'group': 'Professor',
        'is_staff': True,
        'is_superuser': False
    },
    {
        'username': 'admin',
        'email': 'admin@plataformacasa.com',
        'password': 'admin123',
        'first_name': 'Admin',
        'last_name': 'Sistema',
        'group': 'Admin',
        'is_staff': True,
        'is_superuser': True
    }
]

print("=" * 80)
print("CRIANDO GRUPOS E USUÁRIOS DE TESTE")
print("=" * 80)

# Primeiro, criar os grupos se não existirem
grupos_necessarios = ['Aluno', 'Monitor', 'Professor', 'Admin']
for grupo_nome in grupos_necessarios:
    grupo, created = Group.objects.get_or_create(name=grupo_nome)
    if created:
        print(f"✅ Grupo '{grupo_nome}' criado")
    else:
        print(f"ℹ️  Grupo '{grupo_nome}' já existe")

print("\n" + "=" * 80)
print("CRIANDO USUÁRIOS")
print("=" * 80)

for usuario_data in usuarios_teste:
    username = usuario_data['username']
    
    # Verificar se usuário já existe
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        print(f"⚠️  Usuário '{username}' já existe - atualizando grupo...")
        
        # Atualizar grupo
        group = Group.objects.get(name=usuario_data['group'])
        user.groups.clear()
        user.groups.add(group)
        user.is_staff = usuario_data['is_staff']
        user.is_superuser = usuario_data['is_superuser']
        user.save()
        print(f"✅ Atualizado: {username} | Group: {usuario_data['group']}")
        continue
    
    # Criar usuário
    try:
        user = User.objects.create_user(
            username=usuario_data['username'],
            email=usuario_data['email'],
            password=usuario_data['password'],
            first_name=usuario_data['first_name'],
            last_name=usuario_data['last_name']
        )
        
        # Configurar permissões
        user.is_staff = usuario_data['is_staff']
        user.is_superuser = usuario_data['is_superuser']
        user.save()
        
        # Adicionar ao grupo
        group = Group.objects.get(name=usuario_data['group'])
        user.groups.add(group)
        
        print(f"✅ Criado: {username} | Group: {usuario_data['group']} | Email: {usuario_data['email']}")
    
    except Exception as e:
        print(f"❌ Erro ao criar '{username}': {str(e)}")

print("\n" + "=" * 80)
print("PROCESSO CONCLUÍDO")
print("=" * 80)

# Estatísticas finais
total_usuarios = User.objects.count()
print(f"\n📊 Total de usuários no sistema: {total_usuarios}")
for grupo_nome in grupos_necessarios:
    count = User.objects.filter(groups__name=grupo_nome).count()
    print(f"   - {grupo_nome}: {count} usuário(s)")
