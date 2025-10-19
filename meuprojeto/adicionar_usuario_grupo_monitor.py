#!/usr/bin/env python
"""
Script para adicionar usuário aprovado ao grupo Monitor

Este script corrige usuários que foram aprovados antes da implementação
automática de adição ao grupo Monitor.

Uso:
    python adicionar_usuario_grupo_monitor.py
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from plataforma_Casa.models import Inscricao, Aluno

User = get_user_model()

def adicionar_monitores_aprovados():
    """
    Encontra todos os candidatos aprovados e adiciona ao grupo Monitor
    """
    print("=" * 70)
    print("  SCRIPT DE CORREÇÃO - ADICIONAR MONITORES AO GRUPO MONITOR")
    print("=" * 70)
    print()
    
    # Buscar todas as inscrições aprovadas
    inscricoes_aprovadas = Inscricao.objects.filter(status='Aprovado')
    
    print(f"📊 Total de inscrições aprovadas: {inscricoes_aprovadas.count()}")
    print()
    
    if inscricoes_aprovadas.count() == 0:
        print("❌ Nenhuma inscrição aprovada encontrada!")
        return
    
    # Garantir que o grupo Monitor existe
    grupo_monitor, created = Group.objects.get_or_create(name='Monitor')
    if created:
        print("✅ Grupo 'Monitor' criado")
    else:
        print("ℹ️  Grupo 'Monitor' já existe")
    print()
    
    sucesso = 0
    erros = 0
    
    for inscricao in inscricoes_aprovadas:
        aluno = inscricao.aluno
        vaga = inscricao.vaga
        
        print(f"─" * 70)
        print(f"📝 Processando: {aluno.nome}")
        print(f"   Email: {aluno.email}")
        print(f"   Vaga: {vaga.nome}")
        
        try:
            # 1. Buscar User pelo email
            try:
                user = User.objects.get(email=aluno.email)
                print(f"   ✓ User encontrado: {user.username}")
            except User.DoesNotExist:
                print(f"   ❌ User não encontrado para email: {aluno.email}")
                erros += 1
                continue
            
            # 2. Verificar se já está no grupo Monitor
            if user.groups.filter(name='Monitor').exists():
                print(f"   ℹ️  Já está no grupo Monitor")
            else:
                # Adicionar ao grupo Monitor
                user.groups.add(grupo_monitor)
                user.save()
                print(f"   ✅ Adicionado ao grupo Monitor")
            
            # 3. Verificar se já está na lista de monitores da vaga
            if vaga.monitores.filter(id=aluno.id).exists():
                print(f"   ℹ️  Já está na lista de monitores da vaga")
            else:
                # Adicionar à lista de monitores
                vaga.monitores.add(aluno)
                print(f"   ✅ Adicionado à lista de monitores da vaga")
            
            # Mostrar grupos atuais do usuário
            grupos = ", ".join(user.groups.values_list('name', flat=True))
            print(f"   📋 Grupos atuais: {grupos}")
            
            sucesso += 1
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            erros += 1
    
    print()
    print("=" * 70)
    print("  RESUMO")
    print("=" * 70)
    print(f"✅ Processados com sucesso: {sucesso}")
    print(f"❌ Erros: {erros}")
    print(f"📊 Total: {inscricoes_aprovadas.count()}")
    print()
    
    if sucesso > 0:
        print("🎉 Os usuários agora têm permissões de Monitor!")
        print("💡 Eles precisam fazer logout e login novamente para ver o menu.")
    

if __name__ == '__main__':
    try:
        adicionar_monitores_aprovados()
    except KeyboardInterrupt:
        print("\n\n⚠️  Script interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
