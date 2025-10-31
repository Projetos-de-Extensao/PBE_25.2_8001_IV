#!/usr/bin/env python3
"""
Script de teste para todos os endpoints da API Plataforma CASA
Execute: python test_api_endpoints.py
"""

import requests
import json
from datetime import date, datetime

BASE_URL = "http://localhost:8000/api"

def print_section(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def test_endpoint(method, url, data=None, description=""):
    """Testa um endpoint e exibe o resultado"""
    full_url = f"{BASE_URL}{url}"
    print(f"\n[{method}] {full_url}")
    if description:
        print(f"Descrição: {description}")
    
    try:
        if method == "GET":
            response = requests.get(full_url)
        elif method == "POST":
            response = requests.post(full_url, json=data)
        elif method == "PUT":
            response = requests.put(full_url, json=data)
        elif method == "PATCH":
            response = requests.patch(full_url, json=data)
        elif method == "DELETE":
            response = requests.delete(full_url)
        
        print(f"Status: {response.status_code}")
        if response.status_code < 300:
            print("✅ Sucesso!")
            if response.content:
                result = response.json()
                if isinstance(result, list):
                    print(f"Total de itens: {len(result)}")
                else:
                    print(f"Resposta: {json.dumps(result, indent=2, ensure_ascii=False)[:200]}...")
        else:
            print(f"❌ Erro: {response.text[:200]}")
        
        return response
    except Exception as e:
        print(f"❌ Exceção: {str(e)}")
        return None

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                                                                       ║
    ║       🚀 TESTE COMPLETO DOS ENDPOINTS DA API PLATAFORMA CASA 🚀      ║
    ║                                                                       ║
    ║  Este script testa todos os endpoints disponíveis na API             ║
    ║  Certifique-se de que o servidor está rodando em localhost:8000      ║
    ║                                                                       ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Teste de conexão
    print_section("TESTE DE CONEXÃO")
    try:
        response = requests.get(f"{BASE_URL}/")
        print("✅ Servidor está respondendo!")
    except:
        print("❌ Erro: Servidor não está acessível. Execute 'python manage.py runserver'")
        return
    
    # ========================================================================
    # TESTES DE ENDPOINTS BASE
    # ========================================================================
    
    print_section("1. TIPOS DE USUÁRIO")
    test_endpoint("GET", "/tipos-usuario/", description="Lista todos os tipos")
    test_endpoint("GET", "/tipos-usuario/ativos/", description="Lista apenas ativos")
    
    print_section("2. CURSOS")
    test_endpoint("GET", "/cursos/", description="Lista todos os cursos")
    test_endpoint("GET", "/cursos/ativos/", description="Lista apenas ativos")
    response = test_endpoint("GET", "/cursos/")
    if response and response.status_code == 200:
        cursos = response.json()
        if cursos and 'results' in cursos and cursos['results']:
            curso_id = cursos['results'][0]['id']
            test_endpoint("GET", f"/cursos/{curso_id}/", description="Detalhes do curso")
            test_endpoint("GET", f"/cursos/{curso_id}/estatisticas/", description="Estatísticas")
    
    print_section("3. SALAS")
    test_endpoint("GET", "/salas/", description="Lista todas as salas")
    test_endpoint("GET", "/salas/disponiveis/", description="Lista apenas disponíveis")
    
    # ========================================================================
    # TESTES DE USUÁRIOS
    # ========================================================================
    
    print_section("4. USUÁRIOS")
    test_endpoint("GET", "/usuarios/", description="Lista todos os usuários")
    
    print_section("5. FUNCIONÁRIOS")
    test_endpoint("GET", "/funcionarios/", description="Lista todos os funcionários")
    test_endpoint("GET", "/funcionarios/coordenadores/", description="Lista coordenadores")
    
    print_section("6. ALUNOS")
    test_endpoint("GET", "/alunos/", description="Lista todos os alunos")
    test_endpoint("GET", "/alunos/monitores/", description="Lista alunos monitores")
    response = test_endpoint("GET", "/alunos/")
    if response and response.status_code == 200:
        alunos = response.json()
        if alunos and 'results' in alunos and alunos['results']:
            aluno_id = alunos['results'][0]['id']
            test_endpoint("GET", f"/alunos/{aluno_id}/desempenho/", description="Desempenho acadêmico")
    
    # ========================================================================
    # TESTES DE VAGAS E TURMAS
    # ========================================================================
    
    print_section("7. VAGAS")
    test_endpoint("GET", "/vagas/", description="Lista todas as vagas")
    test_endpoint("GET", "/vagas/ativas/", description="Lista vagas ativas")
    test_endpoint("GET", "/vagas/com_vagas_disponiveis/", description="Vagas disponíveis")
    response = test_endpoint("GET", "/vagas/")
    if response and response.status_code == 200:
        vagas = response.json()
        if vagas and 'results' in vagas and vagas['results']:
            vaga_id = vagas['results'][0]['id']
            test_endpoint("GET", f"/vagas/{vaga_id}/inscricoes/", description="Inscrições da vaga")
    
    print_section("8. TURMAS")
    test_endpoint("GET", "/turmas/", description="Lista todas as turmas")
    test_endpoint("GET", "/turmas/ativas/", description="Lista turmas ativas")
    test_endpoint("GET", "/turmas/por_periodo/", description="Turmas no período atual")
    response = test_endpoint("GET", "/turmas/")
    if response and response.status_code == 200:
        turmas = response.json()
        if turmas and 'results' in turmas and turmas['results']:
            turma_id = turmas['results'][0]['id']
            test_endpoint("GET", f"/turmas/{turma_id}/participantes/", description="Participantes")
            test_endpoint("GET", f"/turmas/{turma_id}/presencas/", description="Presenças")
            test_endpoint("GET", f"/turmas/{turma_id}/materiais/", description="Materiais")
    
    # ========================================================================
    # TESTES DE PARTICIPAÇÃO E PRESENÇA
    # ========================================================================
    
    print_section("9. PARTICIPAÇÕES")
    test_endpoint("GET", "/participacoes/", description="Lista todas as participações")
    
    print_section("10. PRESENÇAS")
    test_endpoint("GET", "/presencas/", description="Lista todas as presenças")
    test_endpoint("GET", "/presencas/por_data/?data=2025-10-31", description="Presenças por data")
    
    # ========================================================================
    # TESTES DE INSCRIÇÕES E DOCUMENTOS
    # ========================================================================
    
    print_section("11. INSCRIÇÕES")
    test_endpoint("GET", "/inscricoes/", description="Lista todas as inscrições")
    test_endpoint("GET", "/inscricoes/por_status/?status=Pendente", description="Por status")
    
    print_section("12. DOCUMENTOS")
    test_endpoint("GET", "/documentos/", description="Lista todos os documentos")
    
    # ========================================================================
    # TESTES DE HORAS E PAGAMENTOS
    # ========================================================================
    
    print_section("13. REGISTRO DE HORAS")
    test_endpoint("GET", "/registro-horas/", description="Lista todos os registros")
    test_endpoint("GET", "/registro-horas/pendentes/", description="Registros pendentes")
    
    print_section("14. PAGAMENTOS")
    test_endpoint("GET", "/pagamentos/", description="Lista todos os pagamentos")
    test_endpoint("GET", "/pagamentos/pendentes/", description="Pagamentos pendentes")
    
    # ========================================================================
    # TESTES DE MATERIAIS E ESTATÍSTICAS
    # ========================================================================
    
    print_section("15. MATERIAIS DE APOIO")
    test_endpoint("GET", "/materiais/", description="Lista todos os materiais")
    test_endpoint("GET", "/materiais/publicados/", description="Materiais publicados")
    
    print_section("16. ESTATÍSTICAS")
    test_endpoint("GET", "/estatisticas/geral/", description="Estatísticas gerais do sistema")
    
    # ========================================================================
    # RESUMO FINAL
    # ========================================================================
    
    print("\n\n")
    print("="*80)
    print("  ✅ TESTE COMPLETO FINALIZADO!")
    print("="*80)
    print("""
    📊 Todos os endpoints foram testados!
    
    Para ver a documentação interativa completa:
    👉 http://localhost:8000/restapi/
    
    Para testar com interface gráfica:
    👉 http://localhost:8000/restapi/ (Swagger UI)
    👉 http://localhost:8000/restapi/redoc/ (ReDoc)
    
    Para ver o guia completo de endpoints:
    👉 API_ENDPOINTS_GUIDE.md
    """)

if __name__ == "__main__":
    main()
