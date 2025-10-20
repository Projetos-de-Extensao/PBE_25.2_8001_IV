"""
================================================================================
SCRIPT DE CRIAÇÃO DE USUÁRIOS DE TESTE
================================================================================

Este script cria usuários de teste no sistema com diferentes roles:
- Aluno
- Monitor
- Professor
- Admin

Uso:
    python criar_usuarios_teste.py

Nota: Execute este script no ambiente de produção usando:
    heroku run "python meuprojeto/manage.py shell < criar_usuarios_teste.py"

================================================================================
"""

from django.contrib.auth import get_user_model
from plataforma_Casa.models import Curso

User = get_user_model()

# Dados dos usuários de teste
usuarios_teste = [
    {
        'username': 'aluno.teste',
        'email': 'aluno.teste@plataformacasa.com',
        'password': 'aluno123',
        'first_name': 'Aluno',
        'last_name': 'Teste',
        'role': 1,  # Aluno
        'is_staff': False,
        'is_superuser': False
    },
    {
        'username': 'monitor.teste',
        'email': 'monitor.teste@plataformacasa.com',
        'password': 'monitor123',
        'first_name': 'Monitor',
        'last_name': 'Teste',
        'role': 2,  # Monitor
        'is_staff': False,
        'is_superuser': False
    },
    {
        'username': 'professor.teste',
        'email': 'professor.teste@plataformacasa.com',
        'password': 'professor123',
        'first_name': 'Professor',
        'last_name': 'Teste',
        'role': 3,  # Professor
        'is_staff': True,
        'is_superuser': False
    },
    {
        'username': 'admin',
        'email': 'admin@plataformacasa.com',
        'password': 'admin123',
        'first_name': 'Admin',
        'last_name': 'Sistema',
        'role': 4,  # Admin
        'is_staff': True,
        'is_superuser': True
    }
]

print("=" * 80)
print("CRIANDO USUÁRIOS DE TESTE")
print("=" * 80)

for usuario_data in usuarios_teste:
    username = usuario_data['username']
    
    # Verificar se usuário já existe
    if User.objects.filter(username=username).exists():
        print(f"⚠️  Usuário '{username}' já existe - pulando...")
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
        
        # Configurar role e permissões
        user.role = usuario_data['role']
        user.is_staff = usuario_data['is_staff']
        user.is_superuser = usuario_data['is_superuser']
        user.save()
        
        # Determinar nome do role
        role_names = {1: 'Aluno', 2: 'Monitor', 3: 'Professor', 4: 'Admin'}
        role_name = role_names.get(usuario_data['role'], 'Desconhecido')
        
        print(f"✅ Criado: {username} | Role: {role_name} | Email: {usuario_data['email']}")
    
    except Exception as e:
        print(f"❌ Erro ao criar '{username}': {str(e)}")

print("=" * 80)
print("PROCESSO CONCLUÍDO")
print("=" * 80)

# Estatísticas finais
total_usuarios = User.objects.count()
print(f"\n📊 Total de usuários no sistema: {total_usuarios}")
print(f"   - Alunos: {User.objects.filter(role=1).count()}")
print(f"   - Monitores: {User.objects.filter(role=2).count()}")
print(f"   - Professores: {User.objects.filter(role=3).count()}")
print(f"   - Admins: {User.objects.filter(role=4).count()}")
