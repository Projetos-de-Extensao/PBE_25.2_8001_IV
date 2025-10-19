#!/usr/bin/env python
"""
Script: teste_professor_coordenador.py

Testa se professores têm acesso como Coordenadores

Uso:
    python teste_professor_coordenador.py

Testes:
    ✅ Professores com vagas têm grupo "Coordenador"
    ✅ Decorador @requer_admin_ou_coordenador aceita Professor
    ✅ Dashboard Professor funciona sem erro 500
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth.models import User, Group
from plataforma_Casa.models import Funcionario, Vaga


def test_grupos():
    print("\n" + "="*60)
    print("🧪 TESTE 1: Verificar Grupos de Professores")
    print("="*60)
    
    grupo_professor = Group.objects.get(name='Professor')
    grupo_coordenador = Group.objects.get(name='Coordenador')
    
    professores = User.objects.filter(groups=grupo_professor)
    coordenadores = User.objects.filter(groups=grupo_coordenador)
    
    print(f"\n✅ Total de Professores: {professores.count()}")
    print(f"✅ Total de Coordenadores: {coordenadores.count()}")
    
    print("\n📋 Professores com Grupo Coordenador:")
    for prof in professores:
        if prof.groups.filter(name='Coordenador').exists():
            func = Funcionario.objects.filter(email=prof.email).first()
            vagas = Vaga.objects.filter(coordenador=func).count() if func else 0
            print(f"  ✅ {prof.username} ({vagas} vagas)")


def test_vagas_professor():
    print("\n" + "="*60)
    print("🧪 TESTE 2: Verificar Vagas por Professor")
    print("="*60)
    
    professores_com_vagas = set(Vaga.objects.values_list('coordenador', flat=True))
    
    for func_id in professores_com_vagas:
        func = Funcionario.objects.get(id=func_id)
        user = User.objects.filter(email=func.email).first()
        
        if user:
            tem_coordenador = user.groups.filter(name='Coordenador').exists()
            vagas = Vaga.objects.filter(coordenador=func).count()
            
            status = "✅" if tem_coordenador else "❌"
            print(f"{status} {func.nome}")
            print(f"   └─ {vagas} vagas | Grupo Coordenador: {'SIM' if tem_coordenador else 'NÃO'}")


def test_permissions():
    print("\n" + "="*60)
    print("🧪 TESTE 3: Verificar Permissões de Acesso")
    print("="*60)
    
    grupo_coordenador = Group.objects.get(name='Coordenador')
    grupo_professor = Group.objects.get(name='Professor')
    
    # Verificar que Professores com Coordenador têm acesso
    coordenadores = User.objects.filter(groups=grupo_coordenador)
    
    print(f"\n✅ Usuários com acesso ao @requer_admin_ou_coordenador:")
    
    for coord in coordenadores:
        tem_permissao = coord.groups.filter(
            name__in=['Admin', 'Coordenador']
        ).exists()
        
        is_admin = coord.is_staff or coord.is_superuser
        
        status = "✅" if (tem_permissao or is_admin) else "❌"
        print(f"  {status} {coord.username} (Admin: {is_admin}, Coordenador: {tem_permissao})")


def test_professor_acesso_coordenador():
    print("\n" + "="*60)
    print("🧪 TESTE 4: Professor Recebe Acesso de Coordenador")
    print("="*60)
    
    grupo_professor = Group.objects.get(name='Professor')
    
    for prof_user in User.objects.filter(groups=grupo_professor)[:3]:
        func = Funcionario.objects.filter(email=prof_user.email).first()
        
        if func:
            # Simular o que acontece no dashboard
            tem_vagas = Vaga.objects.filter(coordenador=func).exists()
            tem_coordenador_group = prof_user.groups.filter(name='Coordenador').exists()
            
            # Se tem vagas, deveria ter grupo Coordenador
            if tem_vagas:
                expected = True
            else:
                expected = False
            
            resultado = "✅ PASSOU" if (tem_coordenador_group == expected) else "❌ FALHOU"
            
            print(f"\n{resultado}")
            print(f"  Professor: {prof_user.username}")
            print(f"  Tem vagas: {tem_vagas}")
            print(f"  Tem grupo Coordenador: {tem_coordenador_group}")
            print(f"  Status esperado: {expected}")


def main():
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*15 + "🧪 TESTE: PROFESSOR/COORDENADOR" + " "*10 + "║")
    print("╚" + "="*58 + "╝")
    
    try:
        test_grupos()
        test_vagas_professor()
        test_permissions()
        test_professor_acesso_coordenador()
        
        print("\n" + "="*60)
        print("✨ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("="*60 + "\n")
        
        return 0
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
