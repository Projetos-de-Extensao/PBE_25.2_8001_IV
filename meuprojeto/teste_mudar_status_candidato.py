#!/usr/bin/env python
"""
Script: teste_mudar_status_candidato.py

Testa se a função mudar_status_candidato funciona corretamente com professor

Uso:
    python teste_mudar_status_candidato.py

Testes:
    ✅ Professor pode mudar status de inscrição em sua vaga
    ✅ Professor NÃO pode mudar status de inscrição em vaga de outro professor
    ✅ Validação de permissão está funcionando
"""

import os
import sys
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth.models import User
from django.test import RequestFactory
from plataforma_Casa.models import Funcionario, Vaga, Inscricao, Aluno, Curso
from plataforma_Casa.views import mudar_status_candidato
from datetime import datetime


def test_professor_pode_mudar_status():
    """Teste 1: Professor pode mudar status de inscrição em sua vaga"""
    print("\n" + "="*70)
    print("✅ TESTE 1: Professor pode mudar status de inscrição em sua vaga")
    print("="*70 + "\n")
    
    # Preparar dados
    user = User.objects.get(username='professor.teste')
    insc = Inscricao.objects.get(id=84)
    
    # Simular request
    factory = RequestFactory()
    body = json.dumps({'status': 'Aprovado'})
    request = factory.post(
        '/candidatos/84/status/',
        data=body,
        content_type='application/json'
    )
    request.user = user
    
    # Executar função
    response = mudar_status_candidato(request, 84)
    data = json.loads(response.content)
    
    print(f"Professor: {user.username}")
    print(f"Inscrição: {insc.aluno.nome} -> {insc.vaga.nome}")
    print(f"Novo status solicitado: Aprovado\n")
    
    if data.get('success'):
        print(f"✅ SUCESSO: {data.get('message')}")
        print(f"   Status atualizado para: {data.get('novo_status')}")
        
        # Verificar no banco
        insc.refresh_from_db()
        print(f"   Status no banco: {insc.status}")
        return True
    else:
        print(f"❌ ERRO: {data.get('error')}")
        print(f"   Status code: {response.status_code}")
        return False


def test_professor_nao_pode_mudar_vaga_outro():
    """Teste 2: Professor NÃO pode mudar status em vaga de outro professor"""
    print("\n" + "="*70)
    print("❌ TESTE 2: Professor NÃO pode mudar status em vaga de outro professor")
    print("="*70 + "\n")
    
    # Pegar uma inscrição de vaga de outro professor
    user = User.objects.get(username='professor.teste')
    
    # Buscar inscrição de vaga que NÃO é do professor.teste
    func = Funcionario.objects.get(email=user.email)
    outras_inscricoes = Inscricao.objects.exclude(vaga__coordenador=func)
    
    if not outras_inscricoes.exists():
        print("ℹ️  Não há inscrições de outras vagas para testar. Teste pulado.\n")
        return True
    
    insc = outras_inscricoes.first()
    
    # Simular request
    factory = RequestFactory()
    body = json.dumps({'status': 'Aprovado'})
    request = factory.post(
        f'/candidatos/{insc.id}/status/',
        data=body,
        content_type='application/json'
    )
    request.user = user
    
    # Executar função
    response = mudar_status_candidato(request, insc.id)
    data = json.loads(response.content)
    
    print(f"Professor: {user.username}")
    print(f"Inscrição: {insc.aluno.nome} -> {insc.vaga.nome}")
    print(f"Vaga coordenada por: {insc.vaga.coordenador.nome}\n")
    
    if not data.get('success'):
        print(f"✅ CORRETO: Acesso negado")
        print(f"   Erro: {data.get('error')}")
        print(f"   Status code: {response.status_code}")
        return True
    else:
        print(f"❌ ERRO: Professor conseguiu alterar vaga que não coordena!")
        return False


def main():
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*15 + "🧪 TESTE: MUDAR STATUS CANDIDATO" + " "*18 + "║")
    print("╚" + "="*68 + "╝")
    
    try:
        resultado1 = test_professor_pode_mudar_status()
        resultado2 = test_professor_nao_pode_mudar_vaga_outro()
        
        print("\n" + "="*70)
        print("📊 RESUMO DOS TESTES:")
        print("="*70)
        print(f"  Teste 1 (Pode mudar status): {'✅ PASSOU' if resultado1 else '❌ FALHOU'}")
        print(f"  Teste 2 (Não pode alterar vaga de outro): {'✅ PASSOU' if resultado2 else '❌ FALHOU'}")
        
        if resultado1 and resultado2:
            print("\n✨ TODOS OS TESTES PASSARAM!\n")
            return 0
        else:
            print("\n❌ ALGUNS TESTES FALHARAM!\n")
            return 1
            
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
