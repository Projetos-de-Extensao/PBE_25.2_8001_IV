#!/usr/bin/env python
"""
Script para atualizar todos os pagamentos existentes para tipo 'semestre'
com valor fixo de R$1.500,00
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

from plataforma_Casa.models import StatusPagamento
from decimal import Decimal
from datetime import datetime

def atualizar_pagamentos():
    """Atualiza todos os pagamentos para tipo semestre com valor fixo de R$1500"""
    
    print("\n" + "="*70)
    print("🔄 ATUALIZANDO PAGAMENTOS PARA TIPO SEMESTRE COM VALOR FIXO DE R$1.500")
    print("="*70 + "\n")
    
    # Buscar todos os pagamentos
    pagamentos = StatusPagamento.objects.all()
    total = pagamentos.count()
    
    if total == 0:
        print("❌ Nenhum pagamento encontrado no sistema!")
        return
    
    print(f"📊 Total de pagamentos a atualizar: {total}\n")
    
    atualizados = 0
    erros = 0
    
    for i, pagamento in enumerate(pagamentos, 1):
        try:
            # Armazenar valores antigos
            tipo_antigo = pagamento.tipo_pagamento
            total_horas_antigo = pagamento.total_horas
            valor_hora_antigo = pagamento.valor_hora
            valor_total_antigo = pagamento.valor_total
            obs_antiga = pagamento.observacao
            
            # Atualizar para tipo semestre
            pagamento.tipo_pagamento = 'semestre'
            pagamento.total_horas = Decimal('0')
            pagamento.valor_hora = Decimal('0')
            
            # Atualizar observação
            if obs_antiga and 'Pagamento referente a' in obs_antiga:
                # Substituir observação antiga
                pagamento.observacao = f'Pagamento fixo de semestre: R$ 1.500,00 - Pago ao final do semestre quando o programa {pagamento.turma.nome} encerra (Atualizado em {datetime.now().strftime("%d/%m/%Y")})'
            elif obs_antiga:
                # Manter observação e adicionar nota
                pagamento.observacao = f'{obs_antiga} [Atualizado para tipo semestre - R$1.500,00 em {datetime.now().strftime("%d/%m/%Y")}]'
            else:
                pagamento.observacao = f'Pagamento fixo de semestre: R$ 1.500,00 - Pago ao final do semestre quando o programa {pagamento.turma.nome} encerra'
            
            pagamento.save()
            atualizados += 1
            
            # Exibir progresso
            print(f"[{i}/{total}] ✅ {pagamento.monitor.nome} - {pagamento.mes_referencia.strftime('%m/%Y')}")
            print(f"      Tipo: {tipo_antigo} → {pagamento.tipo_pagamento}")
            print(f"      Valor: R$ {valor_total_antigo:.2f} → R$ {pagamento.valor_total:.2f}")
            
        except Exception as e:
            erros += 1
            print(f"[{i}/{total}] ❌ ERRO ao atualizar {pagamento.monitor.nome}: {str(e)}")
    
    print("\n" + "="*70)
    print("✅ RESUMO DA ATUALIZAÇÃO")
    print("="*70)
    print(f"✅ Pagamentos atualizados: {atualizados}")
    print(f"❌ Erros: {erros}")
    print(f"📊 Total processado: {atualizados + erros}/{total}")
    
    if atualizados == total:
        print("\n🎉 SUCESSO! Todos os pagamentos foram atualizados para tipo SEMESTRE com valor fixo de R$1.500,00")
    elif erros > 0:
        print(f"\n⚠️  {erros} pagamento(s) tiveram erro durante a atualização.")
    
    print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    atualizar_pagamentos()
