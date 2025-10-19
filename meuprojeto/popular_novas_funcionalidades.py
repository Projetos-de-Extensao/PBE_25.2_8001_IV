"""
Script para popular o banco de dados com dados de teste para as novas funcionalidades
Executar: python popular_novas_funcionalidades.py
"""

import os
import django
from datetime import date, time, datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

from plataforma_Casa.models import (
    TipoUsuario, Curso, Usuario, Funcionario, Aluno, Sala, Vaga, 
    Turma, Inscricao, Documento, RegistroHoras, StatusPagamento
)

def limpar_dados_teste():
    """Remove dados de teste anteriores"""
    print("🗑️  Limpando dados de teste anteriores...")
    StatusPagamento.objects.all().delete()
    RegistroHoras.objects.all().delete()
    Documento.objects.all().delete()
    print("✅ Dados de teste limpos!")

def criar_vagas_aprimoradas():
    """Cria vagas com os novos campos"""
    print("\n📋 Criando vagas aprimoradas...")
    
    # Buscar dados necessários
    curso_si = Curso.objects.get(nome='Sistemas de Informação')
    curso_ads = Curso.objects.get(nome='Análise e Desenvolvimento de Sistemas')
    coordenador = Funcionario.objects.filter(coordenador=True).first()
    
    if not coordenador:
        print("❌ Erro: Nenhum coordenador encontrado!")
        return
    
    # Vaga 1: Programação Web
    vaga1, created = Vaga.objects.get_or_create(
        nome='Monitor de Programação Web',
        curso=curso_si,
        defaults={
            'coordenador': coordenador,
            'descricao': 'Vaga para monitoria de Programação Web com foco em HTML, CSS, JavaScript e frameworks modernos.',
            'requisitos': 'CR mínimo de 7.0, ter cursado Programação Web com aprovação, conhecimento em React ou Vue.js',
            'responsabilidades': 'Auxiliar alunos em exercícios práticos, tirar dúvidas sobre conceitos de desenvolvimento web, conduzir sessões de revisão antes das provas, manter repositório de exemplos de código.',
            'numero_vagas': 2,
            'disciplina': 'Programação Web',
            'ativo': True
        }
    )
    print(f"   {'✅ Criada' if created else '📝 Atualizada'}: {vaga1.nome}")
    
    # Vaga 2: Banco de Dados
    vaga2, created = Vaga.objects.get_or_create(
        nome='Monitor de Banco de Dados',
        curso=curso_ads,
        defaults={
            'coordenador': coordenador,
            'descricao': 'Monitoria de Banco de Dados com foco em SQL, modelagem e otimização de queries.',
            'requisitos': 'CR mínimo de 6.5, domínio de SQL, experiência com PostgreSQL ou MySQL',
            'responsabilidades': 'Auxiliar em exercícios de SQL, explicar conceitos de normalização, ajudar na modelagem de bancos de dados, revisar queries dos alunos.',
            'numero_vagas': 1,
            'disciplina': 'Banco de Dados',
            'ativo': True
        }
    )
    print(f"   {'✅ Criada' if created else '📝 Atualizada'}: {vaga2.nome}")
    
    # Vaga 3: Estruturas de Dados
    vaga3, created = Vaga.objects.get_or_create(
        nome='Monitor de Estruturas de Dados',
        curso=curso_si,
        defaults={
            'coordenador': coordenador,
            'descricao': 'Vaga para monitoria de Estruturas de Dados com foco em algoritmos e complexidade.',
            'requisitos': 'CR mínimo de 7.5, excelente domínio de algoritmos, conhecimento em Python ou Java',
            'responsabilidades': 'Explicar estruturas de dados (listas, pilhas, filas, árvores), auxiliar na implementação de algoritmos, conduzir sessões de resolução de problemas.',
            'numero_vagas': 3,
            'disciplina': 'Estruturas de Dados',
            'ativo': True
        }
    )
    print(f"   {'✅ Criada' if created else '📝 Atualizada'}: {vaga3.nome}")
    
    print(f"✅ {Vaga.objects.count()} vagas no sistema!")
    return [vaga1, vaga2, vaga3]

def criar_inscricoes_com_avaliacao():
    """Cria inscrições com diferentes status de avaliação"""
    print("\n👥 Criando inscrições com avaliações...")
    
    vagas = Vaga.objects.all()
    alunos = Aluno.objects.all()[:10]  # Primeiros 10 alunos
    coordenador = Funcionario.objects.filter(coordenador=True).first()
    
    if not vagas or not alunos:
        print("❌ Erro: Vagas ou alunos não encontrados!")
        return
    
    status_opcoes = ['Aprovado', 'Rejeitado', 'Lista de Espera', 'Pendente']
    contador = 0
    
    for vaga in vagas:
        # Criar 3-5 inscrições por vaga
        for i, aluno in enumerate(alunos[:5]):
            # Evitar duplicatas
            if Inscricao.objects.filter(aluno=aluno, vaga=vaga).exists():
                continue
            
            status = status_opcoes[i % len(status_opcoes)]
            
            inscricao = Inscricao.objects.create(
                aluno=aluno,
                vaga=vaga,
                status=status
            )
            
            contador += 1
            print(f"   ✅ Inscrição criada: {aluno.nome} -> {vaga.nome} ({status})")
    
    print(f"✅ {contador} inscrições criadas!")

def criar_registros_horas():
    """Cria registros de horas trabalhadas"""
    print("\n⏰ Criando registros de horas...")
    
    # Buscar turmas ativas
    turmas = Turma.objects.filter(ativo=True)
    
    if not turmas:
        print("❌ Erro: Nenhuma turma ativa encontrada!")
        return
    
    professor = Funcionario.objects.filter(coordenador=False).first()
    
    contador = 0
    for turma in turmas:
        monitor = turma.monitor
        
        # Criar 5 registros de horas para cada monitor
        for dia in range(1, 6):
            data_registro = date.today() - timedelta(days=dia*7)
            
            registro = RegistroHoras.objects.create(
                turma=turma,
                monitor=monitor,
                data=data_registro,
                hora_inicio=time(14, 0),
                hora_fim=time(16, 0),
                descricao_atividade=f'Monitoria do dia {data_registro.strftime("%d/%m/%Y")}: Auxílio aos alunos em exercícios práticos, esclarecimento de dúvidas sobre conteúdo da disciplina.',
                status=['Aprovado', 'Pendente', 'Rejeitado'][dia % 3],
                validado_por=professor if dia % 3 != 1 else None,
                data_validacao=datetime.now() if dia % 3 != 1 else None,
                observacao_validador='Horas aprovadas conforme esperado.' if dia % 3 == 0 else ('Horário incompatível com agenda.' if dia % 3 == 2 else None)
            )
            
            contador += 1
    
    print(f"✅ {contador} registros de horas criados!")

def criar_pagamentos():
    """Cria registros de pagamento - VALOR FIXO DE R$1500 POR SEMESTRE"""
    print("\n💰 Criando status de pagamentos...")
    
    turmas = Turma.objects.filter(ativo=True)
    
    if not turmas:
        print("❌ Erro: Nenhuma turma ativa encontrada!")
        return
    
    gestor = Funcionario.objects.filter(coordenador=True).first()
    
    contador = 0
    for turma in turmas:
        monitor = turma.monitor
        
        # Criar pagamentos dos últimos 3 meses (final de semestre)
        for mes in range(3):
            mes_ref = date.today() - timedelta(days=30*mes)
            
            # Criar pagamento com valor fixo de semestre
            pagamento = StatusPagamento.objects.create(
                monitor=monitor,
                turma=turma,
                mes_referencia=mes_ref,
                status=['Pago', 'Processando', 'Pendente'][mes],
                processado_por=gestor if mes != 2 else None,
                data_processamento=datetime.now() if mes != 2 else None,
                observacao=f'Pagamento fixo de semestre: R$ 1.500,00 - Pago ao final do semestre quando o programa {turma.nome} encerra'
            )
            
            contador += 1
            print(f"   ✅ Pagamento criado: {monitor.nome} - {mes_ref.strftime('%m/%Y')} - R$ {pagamento.valor_total}")
    
    print(f"✅ {contador} pagamentos criados!")
    
    print(f"✅ {contador} pagamentos criados!")

def criar_avaliacoes_monitores():
    """FUNÇÃO REMOVIDA - Sistema de avaliação de monitor descontinuado"""
    print("\n📊 Sistema de avaliação de monitor foi descontinuado (não há dados a criar)")
    pass

def exibir_resumo():
    """Exibe resumo dos dados criados"""
    print("\n" + "="*60)
    print("📊 RESUMO DOS DADOS CRIADOS")
    print("="*60)
    
    print(f"\n📋 Vagas: {Vaga.objects.count()}")
    print(f"   - Ativas: {Vaga.objects.filter(ativo=True).count()}")
    print(f"   - Com candidatos: {Vaga.objects.filter(inscricao__isnull=False).distinct().count()}")
    
    print(f"\n👥 Inscrições: {Inscricao.objects.count()}")
    print(f"   - Pendentes: {Inscricao.objects.filter(status='Pendente').count()}")
    print(f"   - Aprovadas: {Inscricao.objects.filter(status='Aprovado').count()}")
    print(f"   - Rejeitadas: {Inscricao.objects.filter(status='Rejeitado').count()}")
    print(f"   - Lista de Espera: {Inscricao.objects.filter(status='Lista de Espera').count()}")
    
    print(f"\n⏰ Registros de Horas: {RegistroHoras.objects.count()}")
    print(f"   - Pendentes: {RegistroHoras.objects.filter(status='Pendente').count()}")
    print(f"   - Aprovados: {RegistroHoras.objects.filter(status='Aprovado').count()}")
    print(f"   - Rejeitados: {RegistroHoras.objects.filter(status='Rejeitado').count()}")
    total_horas = sum([r.total_horas for r in RegistroHoras.objects.filter(status='Aprovado')])
    print(f"   - Total de horas aprovadas: {total_horas}h")
    
    print(f"\n💰 Pagamentos: {StatusPagamento.objects.count()}")
    print(f"   - Pendentes: {StatusPagamento.objects.filter(status='Pendente').count()}")
    print(f"   - Processando: {StatusPagamento.objects.filter(status='Processando').count()}")
    print(f"   - Pagos: {StatusPagamento.objects.filter(status='Pago').count()}")
    total_pagar = sum([p.valor_total for p in StatusPagamento.objects.filter(status='Pendente')])
    print(f"   - Total a pagar: R$ {total_pagar:.2f}")
    
    print("\n" + "="*60)

def main():
    """Função principal"""
    print("\n" + "🚀 "*20)
    print("POPULANDO BANCO DE DADOS COM NOVAS FUNCIONALIDADES")
    print("🚀 "*20 + "\n")
    
    try:
        # Limpar dados anteriores
        limpar_dados_teste()
        
        # Criar dados novos
        criar_vagas_aprimoradas()
        criar_inscricoes_com_avaliacao()
        criar_registros_horas()
        criar_pagamentos()
        criar_avaliacoes_monitores()
        
        # Exibir resumo
        exibir_resumo()
        
        print("\n✅ Processo concluído com sucesso!")
        print("\n📌 Próximos passos:")
        print("   1. Acesse http://localhost:8000/portal-vagas/ para ver o portal")
        print("   2. Acesse http://localhost:8000/gestao/dashboard/ para o dashboard de gestão")
        print("   3. Acesse http://localhost:8000/admin/ para gerenciar no admin")
        
    except Exception as e:
        print(f"\n❌ Erro durante a execução: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
