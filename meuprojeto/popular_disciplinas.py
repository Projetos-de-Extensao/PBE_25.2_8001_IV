#!/usr/bin/env python3
"""
Script para popular o banco de dados com disciplinas pré-cadastradas
Execute: python manage.py shell < popular_disciplinas.py
Ou: python3 popular_disciplinas.py (se configurado manage.py path)
"""

import os
import django

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

from plataforma_Casa.models import Curso, Disciplina, Funcionario

def popular_disciplinas():
    """Popula o banco com disciplinas pré-cadastradas de diversos cursos"""
    
    print("="*80)
    print(" POPULANDO DISCIPLINAS PRÉ-CADASTRADAS")
    print("="*80)
    
    # Buscar ou criar cursos
    curso_cc, _ = Curso.objects.get_or_create(
        nome="Ciência da Computação",
        defaults={'ativo': True}
    )
    
    curso_ads, _ = Curso.objects.get_or_create(
        nome="Análise e Desenvolvimento de Sistemas",
        defaults={'ativo': True}
    )
    
    curso_si, _ = Curso.objects.get_or_create(
        nome="Sistemas de Informação",
        defaults={'ativo': True}
    )
    
    # Buscar um funcionário para ser o criador (opcional)
    criador = Funcionario.objects.filter(funcao='Professor').first()
    
    # ========================================================================
    # DISCIPLINAS DE CIÊNCIA DA COMPUTAÇÃO
    # ========================================================================
    
    disciplinas_cc = [
        {
            'codigo': 'CC101',
            'nome': 'Introdução à Programação',
            'curso': curso_cc,
            'carga_horaria': 80,
            'periodo_sugerido': 1,
            'ementa': 'Introdução aos conceitos básicos de programação. Algoritmos, estruturas de controle, funções.',
        },
        {
            'codigo': 'CC102',
            'nome': 'Lógica de Programação',
            'curso': curso_cc,
            'carga_horaria': 60,
            'periodo_sugerido': 1,
            'ementa': 'Desenvolvimento do raciocínio lógico. Resolução de problemas computacionais.',
        },
        {
            'codigo': 'CC103',
            'nome': 'Matemática Discreta',
            'curso': curso_cc,
            'carga_horaria': 80,
            'periodo_sugerido': 1,
            'ementa': 'Conjuntos, lógica proposicional, teoria dos grafos, combinatória.',
        },
        {
            'codigo': 'CC201',
            'nome': 'Estruturas de Dados',
            'curso': curso_cc,
            'carga_horaria': 80,
            'periodo_sugerido': 2,
            'ementa': 'Estruturas de dados fundamentais: listas, pilhas, filas, árvores.',
        },
        {
            'codigo': 'CC202',
            'nome': 'Programação Orientada a Objetos',
            'curso': curso_cc,
            'carga_horaria': 80,
            'periodo_sugerido': 2,
            'ementa': 'Paradigma orientado a objetos. Classes, herança, polimorfismo, encapsulamento.',
        },
        {
            'codigo': 'CC203',
            'nome': 'Algoritmos e Complexidade',
            'curso': curso_cc,
            'carga_horaria': 80,
            'periodo_sugerido': 3,
            'ementa': 'Análise de algoritmos, notação Big O, algoritmos de ordenação e busca.',
        },
        {
            'codigo': 'CC301',
            'nome': 'Banco de Dados',
            'curso': curso_cc,
            'carga_horaria': 80,
            'periodo_sugerido': 3,
            'ementa': 'Modelagem de dados, SQL, normalização, transações.',
        },
        {
            'codigo': 'CC302',
            'nome': 'Engenharia de Software',
            'curso': curso_cc,
            'carga_horaria': 80,
            'periodo_sugerido': 4,
            'ementa': 'Processos de desenvolvimento, requisitos, projeto, testes.',
        },
        {
            'codigo': 'CC303',
            'nome': 'Redes de Computadores',
            'curso': curso_cc,
            'carga_horaria': 80,
            'periodo_sugerido': 4,
            'ementa': 'Arquitetura de redes, protocolos TCP/IP, redes locais e de longa distância.',
        },
        {
            'codigo': 'CC401',
            'nome': 'Sistemas Operacionais',
            'curso': curso_cc,
            'carga_horaria': 80,
            'periodo_sugerido': 5,
            'ementa': 'Gerenciamento de processos, memória, sistemas de arquivos.',
        },
        {
            'codigo': 'CC402',
            'nome': 'Desenvolvimento Web',
            'curso': curso_cc,
            'carga_horaria': 80,
            'periodo_sugerido': 5,
            'ementa': 'HTML, CSS, JavaScript, frameworks modernos, APIs REST.',
        },
        {
            'codigo': 'CC501',
            'nome': 'Inteligência Artificial',
            'curso': curso_cc,
            'carga_horaria': 80,
            'periodo_sugerido': 6,
            'ementa': 'Agentes inteligentes, busca, aprendizado de máquina, redes neurais.',
        },
    ]
    
    # ========================================================================
    # DISCIPLINAS DE ANÁLISE E DESENVOLVIMENTO DE SISTEMAS
    # ========================================================================
    
    disciplinas_ads = [
        {
            'codigo': 'ADS101',
            'nome': 'Algoritmos',
            'curso': curso_ads,
            'carga_horaria': 80,
            'periodo_sugerido': 1,
            'ementa': 'Lógica de programação, estruturas básicas, resolução de problemas.',
        },
        {
            'codigo': 'ADS102',
            'nome': 'Programação para Web',
            'curso': curso_ads,
            'carga_horaria': 80,
            'periodo_sugerido': 2,
            'ementa': 'HTML5, CSS3, JavaScript, desenvolvimento frontend.',
        },
        {
            'codigo': 'ADS201',
            'nome': 'Banco de Dados Relacionais',
            'curso': curso_ads,
            'carga_horaria': 80,
            'periodo_sugerido': 2,
            'ementa': 'Modelagem ER, SQL, MySQL, PostgreSQL.',
        },
        {
            'codigo': 'ADS202',
            'nome': 'Desenvolvimento de Aplicações',
            'curso': curso_ads,
            'carga_horaria': 80,
            'periodo_sugerido': 3,
            'ementa': 'Frameworks de desenvolvimento, arquitetura MVC, APIs.',
        },
        {
            'codigo': 'ADS301',
            'nome': 'Desenvolvimento Mobile',
            'curso': curso_ads,
            'carga_horaria': 80,
            'periodo_sugerido': 4,
            'ementa': 'Desenvolvimento para Android e iOS, Flutter, React Native.',
        },
    ]
    
    # ========================================================================
    # DISCIPLINAS DE SISTEMAS DE INFORMAÇÃO
    # ========================================================================
    
    disciplinas_si = [
        {
            'codigo': 'SI101',
            'nome': 'Fundamentos de Sistemas de Informação',
            'curso': curso_si,
            'carga_horaria': 60,
            'periodo_sugerido': 1,
            'ementa': 'Conceitos básicos de SI, tipos de sistemas, componentes.',
        },
        {
            'codigo': 'SI102',
            'nome': 'Programação I',
            'curso': curso_si,
            'carga_horaria': 80,
            'periodo_sugerido': 1,
            'ementa': 'Introdução à programação, Python, estruturas básicas.',
        },
        {
            'codigo': 'SI201',
            'nome': 'Análise de Sistemas',
            'curso': curso_si,
            'carga_horaria': 80,
            'periodo_sugerido': 3,
            'ementa': 'Levantamento de requisitos, UML, casos de uso.',
        },
        {
            'codigo': 'SI202',
            'nome': 'Gestão de Projetos',
            'curso': curso_si,
            'carga_horaria': 60,
            'periodo_sugerido': 4,
            'ementa': 'PMBOK, metodologias ágeis, Scrum, gestão de equipes.',
        },
    ]
    
    # Criar disciplinas
    todas_disciplinas = disciplinas_cc + disciplinas_ads + disciplinas_si
    disciplinas_criadas = []
    
    for disc_data in todas_disciplinas:
        disciplina, created = Disciplina.objects.get_or_create(
            codigo=disc_data['codigo'],
            defaults={
                **disc_data,
                'criado_por': criador,
                'ativo': True
            }
        )
        
        if created:
            disciplinas_criadas.append(disciplina)
            print(f"✅ Criada: {disciplina.codigo} - {disciplina.nome}")
        else:
            print(f"⏭️  Já existe: {disciplina.codigo} - {disciplina.nome}")
    
    # ========================================================================
    # CRIAR PRÉ-REQUISITOS
    # ========================================================================
    
    print("\n" + "="*80)
    print(" CONFIGURANDO PRÉ-REQUISITOS")
    print("="*80)
    
    pre_requisitos = [
        ('CC201', ['CC101']),  # Estruturas de Dados precisa de Intro Programação
        ('CC202', ['CC101']),  # POO precisa de Intro Programação
        ('CC203', ['CC201']),  # Algoritmos precisa de Estruturas de Dados
        ('CC301', ['CC201']),  # Banco de Dados precisa de Estruturas de Dados
        ('CC302', ['CC202']),  # Eng. Software precisa de POO
        ('CC401', ['CC203']),  # Sistemas Operacionais precisa de Algoritmos
        ('CC402', ['CC202']),  # Dev Web precisa de POO
        ('CC501', ['CC203', 'CC301']),  # IA precisa de Algoritmos e BD
        ('ADS201', ['ADS101']),  # BD precisa de Algoritmos
        ('ADS202', ['ADS102', 'ADS201']),  # Dev Aplicações precisa de Web e BD
        ('ADS301', ['ADS202']),  # Dev Mobile precisa de Dev Aplicações
        ('SI201', ['SI102']),  # Análise precisa de Programação
        ('SI202', ['SI201']),  # Gestão precisa de Análise
    ]
    
    for codigo_disc, codigos_pre_req in pre_requisitos:
        try:
            disciplina = Disciplina.objects.get(codigo=codigo_disc)
            for codigo_pre in codigos_pre_req:
                pre_req = Disciplina.objects.get(codigo=codigo_pre)
                disciplina.pre_requisitos.add(pre_req)
            print(f"✅ Pré-requisitos configurados para {codigo_disc}")
        except Disciplina.DoesNotExist as e:
            print(f"❌ Erro ao configurar pré-requisito: {e}")
    
    # ========================================================================
    # RESUMO
    # ========================================================================
    
    print("\n" + "="*80)
    print(" RESUMO")
    print("="*80)
    print(f"Total de disciplinas no banco: {Disciplina.objects.count()}")
    print(f"Disciplinas de Ciência da Computação: {Disciplina.objects.filter(curso=curso_cc).count()}")
    print(f"Disciplinas de ADS: {Disciplina.objects.filter(curso=curso_ads).count()}")
    print(f"Disciplinas de SI: {Disciplina.objects.filter(curso=curso_si).count()}")
    print(f"Disciplinas ativas: {Disciplina.objects.filter(ativo=True).count()}")
    print("\n✅ População de disciplinas concluída com sucesso!")
    print("="*80)


if __name__ == '__main__':
    popular_disciplinas()
