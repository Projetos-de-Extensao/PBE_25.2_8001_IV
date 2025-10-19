#!/usr/bin/env python
"""
Script para criar usuário aluno de teste para login no sistema
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

from plataforma_Casa.models import Usuario, TipoUsuario, Aluno, Curso
from django.contrib.auth.hashers import make_password

def criar_aluno_teste():
    """Cria um aluno de teste para login"""
    
    print("=" * 60)
    print("CRIANDO ALUNO DE TESTE")
    print("=" * 60)
    
    # Buscar tipo de usuário Aluno
    try:
        tipo_aluno = TipoUsuario.objects.get(tipo='Aluno')
        print(f"✓ Tipo de usuário 'Aluno' encontrado")
    except TipoUsuario.DoesNotExist:
        print("✗ Tipo de usuário 'Aluno' não encontrado. Criando...")
        tipo_aluno = TipoUsuario.objects.create(
            tipo='Aluno',
            ativo=True
        )
        print(f"✓ Tipo de usuário 'Aluno' criado")
    
    # Buscar um curso
    try:
        curso = Curso.objects.filter(ativo=True).first()
        if not curso:
            raise Curso.DoesNotExist
        print(f"✓ Curso '{curso.nome}' selecionado")
    except Curso.DoesNotExist:
        print("✗ Nenhum curso ativo encontrado. Criando curso de teste...")
        curso = Curso.objects.create(
            nome='Análise e Desenvolvimento de Sistemas',
            descricao='Curso de Tecnologia',
            ativo=True
        )
        print(f"✓ Curso '{curso.nome}' criado")
    
    # Dados do aluno de teste
    email_teste = 'aluno.teste@casa.com'
    senha_teste = 'aluno123'
    
    # Verificar se já existe
    if Usuario.objects.filter(email=email_teste).exists():
        print(f"\n⚠ Usuário com email '{email_teste}' já existe!")
        resposta = input("Deseja recriar? (s/n): ")
        if resposta.lower() != 's':
            print("Operação cancelada.")
            return
        else:
            # Deletar usuário e aluno existentes
            Usuario.objects.filter(email=email_teste).delete()
            Aluno.objects.filter(email=email_teste).delete()
            print("✓ Usuário anterior removido")
    
    # Criar usuário base
    usuario = Usuario.objects.create(
        nome='João da Silva (Teste)',
        email=email_teste,
        tipo_usuario=tipo_aluno,
        ativo=True
    )
    print(f"\n✓ Usuário criado: {usuario.nome}")
    
    # Criar aluno
    from datetime import date
    aluno = Aluno.objects.create(
        nome='João da Silva (Teste)',
        email=email_teste,
        tipo_usuario=tipo_aluno,
        matricula='20250001',
        curso=curso,
        data_ingresso=date(2025, 1, 1),
        periodo=2,
        cr_geral=8.5,
        ativo=True
    )
    print(f"✓ Aluno criado: {aluno.nome}")
    print(f"  - Matrícula: {aluno.matricula}")
    print(f"  - Curso: {aluno.curso.nome}")
    print(f"  - CR: {aluno.cr_geral}")
    
    # Exibir credenciais
    print("\n" + "=" * 60)
    print("ALUNO DE TESTE CRIADO COM SUCESSO!")
    print("=" * 60)
    print(f"\n📧 Email: {email_teste}")
    print(f"🔑 Senha: {senha_teste}")
    print(f"\n🎓 Nome: {aluno.nome}")
    print(f"📝 Matrícula: {aluno.matricula}")
    print(f"📚 Curso: {aluno.curso.nome}")
    print(f"⭐ CR: {aluno.cr_geral}")
    print(f"\n🌐 Acesse: http://localhost:8000/login/")
    print("\n" + "=" * 60)
    
    return aluno

if __name__ == '__main__':
    criar_aluno_teste()
