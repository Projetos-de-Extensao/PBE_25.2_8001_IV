#!/usr/bin/env python
"""
Script para limpar o base.html removendo código duplicado órfão
"""

import re

# Ler o arquivo
with open('plataforma_Casa/templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Encontrar a posição do </nav> e do <main>
nav_close_pos = content.find('</nav>')
main_open_pos = content.find('<main class="main-content"')

if nav_close_pos != -1 and main_open_pos != -1 and nav_close_pos < main_open_pos:
    # Extrair o conteúdo entre </nav> e <main>
    between = content[nav_close_pos + 7:main_open_pos]
    
    # Verificar se há apenas "<!-- Main Content -->" e espaços em branco
    clean_between = between.strip()
    
    if clean_between and clean_between != '<!-- Main Content -->':
        print(f"❌ Encontrado código órfão entre </nav> e <main>:")
        print(f"Tamanho: {len(between)} caracteres")
        print(f"Conteúdo (primeiros 500 chars):\n{between[:500]}")
        
        # Limpar: manter apenas o comentário
        new_content = (
            content[:nav_close_pos + 7] + 
            '\n\n            <!-- Main Content -->\n            ' + 
            content[main_open_pos:]
        )
        
        # Salvar arquivo limpo
        with open('plataforma_Casa/templates/base.html', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("\n✅ Arquivo limpo com sucesso!")
        print(f"Linhas removidas: {content.count(chr(10)) - new_content.count(chr(10))}")
    else:
        print("✅ Não há código órfão - arquivo está limpo!")
else:
    print(f"❌ Erro: não encontrou </nav> ({nav_close_pos}) ou <main> ({main_open_pos})")
