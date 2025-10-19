#!/usr/bin/env python
"""
Script de validação do template base.html
Verifica se não há tags Django dentro de comentários HTML
"""

import re
import sys

def validar_template(caminho_arquivo):
    """
    Valida se o template não contém tags Django dentro de comentários HTML
    """
    print(f"🔍 Validando template: {caminho_arquivo}")
    print("=" * 70)
    
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    # Padrão para detectar tags Django em comentários HTML
    # Busca por <!-- ... {% ... %} ... -->
    padrao = re.compile(r'<!--.*{%.*%}.*-->')
    
    erros_encontrados = []
    
    for num_linha, linha in enumerate(linhas, start=1):
        if padrao.search(linha):
            erros_encontrados.append((num_linha, linha.strip()))
    
    if erros_encontrados:
        print(f"❌ ERRO: Encontradas {len(erros_encontrados)} tags Django em comentários HTML:")
        print()
        for num, conteudo in erros_encontrados:
            print(f"  Linha {num}:")
            print(f"    {conteudo[:100]}...")
            print()
        return False
    else:
        print("✅ SUCESSO: Nenhuma tag Django encontrada em comentários HTML!")
        print()
        print("📊 Estatísticas do arquivo:")
        print(f"   - Total de linhas: {len(linhas)}")
        
        # Contar comentários HTML
        comentarios_html = sum(1 for linha in linhas if '<!--' in linha or '-->' in linha)
        print(f"   - Linhas com comentários HTML: {comentarios_html}")
        
        # Contar tags Django
        tags_django = sum(1 for linha in linhas if '{%' in linha or '%}' in linha)
        print(f"   - Linhas com tags Django: {tags_django}")
        
        # Contar blocos
        blocos = sum(1 for linha in linhas if '{% block' in linha)
        print(f"   - Blocos Django definidos: {blocos}")
        
        return True

if __name__ == '__main__':
    caminho = 'plataforma_Casa/templates/base.html'
    
    try:
        sucesso = validar_template(caminho)
        sys.exit(0 if sucesso else 1)
    except FileNotFoundError:
        print(f"❌ ERRO: Arquivo não encontrado: {caminho}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERRO: {e}")
        sys.exit(1)
