# 📊 Relatórios com Exportação PDF/Excel - Documentação Completa

## ✅ Implementação Concluída

### 📁 Arquivos Criados

#### Templates de Relatórios (3 arquivos)

1. **`templates/relatorios/candidatos_vaga.html`**
   - Relatório de candidatos por vaga
   - Tabela detalhada com informações dos candidatos
   - Filtros por vaga
   - Exportação PDF e Excel

2. **`templates/relatorios/monitores_selecionados.html`**
   - Relatório de monitores aprovados
   - Estatísticas gerais (total, média CR, disciplinas)
   - Gráficos de distribuição (Chart.js)
   - Filtros por curso, vaga e ordenação
   - Exportação completa

3. **`templates/relatorios/horas_trabalhadas.html`**
   - Controle de horas e pagamentos
   - Resumo financeiro
   - Análise por status e período
   - Gráficos de tendências
   - Resumo por monitor
   - Exportação com todos os detalhes

---

## 🎯 Funcionalidades Implementadas

### 1. Exportação em PDF
**Biblioteca:** jsPDF + jsPDF-AutoTable

**Características:**
- ✅ Geração no lado do cliente (JavaScript)
- ✅ Tabelas formatadas automaticamente
- ✅ Cabeçalhos personalizados
- ✅ Orientação landscape para relatórios grandes
- ✅ Paginação automática
- ✅ Estilos customizados

**Exemplo de uso:**
```javascript
function exportarPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF('l', 'mm', 'a4');
    
    doc.setFontSize(18);
    doc.text('Relatório de Monitores Selecionados', 14, 15);
    
    doc.autoTable({
        startY: 30,
        head: [['#', 'Monitor', 'Curso', 'Vaga', 'CR', 'Nota']],
        body: tableData,
        theme: 'grid',
        headStyles: { fillColor: [28, 200, 138] }
    });
    
    doc.save('relatorio.pdf');
}
```

### 2. Exportação em Excel
**Biblioteca:** SheetJS (xlsx)

**Características:**
- ✅ Geração de planilhas .xlsx
- ✅ Múltiplas abas (sheets) quando necessário
- ✅ Formatação de colunas (largura)
- ✅ Dados estruturados
- ✅ Suporte a fórmulas

**Exemplo de uso:**
```javascript
function exportarExcel() {
    const data = [
        ['Relatório de Monitores'],
        ['Gerado em: ' + new Date().toLocaleString()],
        [],
        ['#', 'Monitor', 'Curso', 'Nota'],
        // ... dados
    ];
    
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.aoa_to_sheet(data);
    
    // Definir largura das colunas
    ws['!cols'] = [
        { wch: 5 }, { wch: 25 }, { wch: 30 }, { wch: 8 }
    ];
    
    XLSX.utils.book_append_sheet(wb, ws, 'Monitores');
    XLSX.writeFile(wb, 'relatorio.xlsx');
}
```

### 3. Impressão Direta
**Funcionalidade:** `window.print()`

**Características:**
- ✅ CSS específico para impressão (@media print)
- ✅ Oculta elementos desnecessários (botões, formulários)
- ✅ Formatação otimizada para papel
- ✅ Quebras de página inteligentes

**CSS de Impressão:**
```css
@media print {
    .btn, .card-body form, canvas {
        display: none !important;
    }
    
    .card {
        page-break-inside: avoid;
        border: 1px solid #000;
    }
    
    .card-header {
        background-color: #4e73df !important;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
}
```

---

## 📈 Gráficos e Visualizações

### Chart.js Integrado

#### 1. Relatório de Monitores Selecionados
**Gráficos:**
- 📊 **Pie Chart**: Distribuição por Curso
- 📊 **Bar Chart**: Top 5 Disciplinas

#### 2. Relatório de Horas Trabalhadas
**Gráficos:**
- 📊 **Doughnut Chart**: Horas por Status (Aprovado/Pendente/Rejeitado)
- 📊 **Line Chart**: Evolução Mensal (últimos 6 meses)

**Código de Exemplo:**
```javascript
new Chart(ctx, {
    type: 'pie',
    data: {
        labels: {{ cursos_labels|safe }},
        datasets: [{
            data: {{ cursos_data|safe }},
            backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc']
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { position: 'bottom' }
        }
    }
});
```

---

## 🔄 Views Atualizadas

### 1. `relatorio_candidatos_por_vaga()`
```python
def relatorio_candidatos_por_vaga(request):
    import json
    
    vagas = Vaga.objects.filter(ativo=True).prefetch_related(
        'inscricao_set__aluno__curso',
        'inscricao_set__documentos'
    )
    
    vaga_filtro = request.GET.get('vaga')
    if vaga_filtro:
        vagas = vagas.filter(id=vaga_filtro)
    
    context = {
        'vagas': vagas,
        'now': timezone.now(),
    }
    return render(request, 'relatorios/candidatos_vaga.html', context)
```

**Dados Fornecidos:**
- Lista de vagas com candidatos
- Documentos anexados
- Status das inscrições
- Data de geração

### 2. `relatorio_monitores_selecionados()`
```python
def relatorio_monitores_selecionados(request):
    import json
    from django.db.models import Avg
    
    inscricoes = Inscricao.objects.filter(status='Aprovado').select_related(
        'aluno__curso', 'vaga', 'avaliado_por'
    )
    
    # Filtros
    curso_filtro = request.GET.get('curso')
    vaga_filtro = request.GET.get('vaga')
    ordem = request.GET.get('ordem', 'nome')
    
    # ... filtros aplicados
    
    # Estatísticas
    media_cr = inscricoes.aggregate(media=Avg('aluno__cr_geral'))['media']
    
    # Dados para gráficos
    cursos_labels = json.dumps([...])
    cursos_data = json.dumps([...])
    
    # ... outros dados
```

**Dados Fornecidos:**
- Inscrições aprovadas com filtros
- Estatísticas (média CR, total vagas, disciplinas)
- Dados para gráficos (JSON)
- Listas para filtros

### 3. `relatorio_horas_trabalhadas()`
```python
def relatorio_horas_trabalhadas(request):
    import json
    from django.db.models import Q
    from collections import defaultdict
    
    registros = RegistroHoras.objects.all().select_related(
        'monitor', 'validado_por'
    )
    
    # Filtros múltiplos
    monitor_filtro = request.GET.get('monitor')
    mes_filtro = request.GET.get('mes')
    ano_filtro = request.GET.get('ano')
    status_filtro = request.GET.get('status')
    
    # Estatísticas gerais
    total_horas = registros.aggregate(total=Sum('total_horas'))['total']
    valor_total = registros.aggregate(total=Sum('valor_total'))['total']
    
    # Resumo por monitor
    resumo_por_monitor = registros.values('monitor__nome').annotate(
        total_registros=Count('id'),
        horas_aprovadas=Sum('total_horas', filter=Q(status='Aprovado')),
        valor_total=Sum('valor_total')
    )
    
    # Dados para gráficos (status e mensal)
    # ...
```

**Dados Fornecidos:**
- Registros de horas com filtros
- Estatísticas financeiras
- Resumo por monitor
- Dados para gráficos de status e evolução mensal

---

## 🎨 Interface dos Relatórios

### Componentes Visuais

#### 1. Cards de Estatísticas
```html
<div class="card border-left-primary shadow">
    <div class="card-body">
        <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
            Total de Monitores
        </div>
        <div class="h5 mb-0 font-weight-bold text-gray-800">
            {{ inscricoes.count }}
        </div>
    </div>
</div>
```

#### 2. Botões de Exportação
```html
<div class="btn-group" role="group">
    <button type="button" class="btn btn-danger" onclick="exportarPDF()">
        <i class="fas fa-file-pdf"></i> Exportar PDF
    </button>
    <button type="button" class="btn btn-success" onclick="exportarExcel()">
        <i class="fas fa-file-excel"></i> Exportar Excel
    </button>
    <button type="button" class="btn btn-primary" onclick="window.print()">
        <i class="fas fa-print"></i> Imprimir
    </button>
</div>
```

#### 3. Filtros Avançados
```html
<div class="card mb-4">
    <div class="card-body">
        <form method="get" class="row g-3">
            <div class="col-md-4">
                <label for="curso" class="form-label">Curso</label>
                <select name="curso" id="curso" class="form-select">
                    <option value="">Todos os Cursos</option>
                    {% for curso in cursos %}
                    <option value="{{ curso.id }}">{{ curso.nome }}</option>
                    {% endfor %}
                </select>
            </div>
            <!-- ... outros filtros -->
            <div class="col-md-2 d-flex align-items-end">
                <button type="submit" class="btn btn-primary w-100">
                    <i class="fas fa-filter"></i> Filtrar
                </button>
            </div>
        </form>
    </div>
</div>
```

#### 4. Tabelas Responsivas
```html
<div class="table-responsive">
    <table class="table table-bordered table-hover" id="tabelaMonitores">
        <thead class="table-light">
            <tr>
                <th>#</th>
                <th>Monitor</th>
                <th>Curso</th>
                <!-- ... -->
            </tr>
        </thead>
        <tbody>
            {% for inscricao in inscricoes %}
            <tr>
                <td>{{ forloop.counter }}</td>
                <td><strong>{{ inscricao.aluno.nome }}</strong></td>
                <!-- ... -->
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
```

---

## 📦 Bibliotecas CDN Utilizadas

### JavaScript
```html
<!-- Chart.js para gráficos -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<!-- jsPDF para geração de PDF -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>

<!-- jsPDF-AutoTable para tabelas em PDF -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.31/jspdf.plugin.autotable.min.js"></script>

<!-- SheetJS para geração de Excel -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
```

---

## 🚀 Como Usar

### 1. Acessar Relatórios
```
http://localhost:8000/relatorios/candidatos-vaga/
http://localhost:8000/relatorios/monitores-selecionados/
http://localhost:8000/relatorios/horas-trabalhadas/
```

### 2. Aplicar Filtros
- Selecione os filtros desejados nos formulários
- Clique em "Filtrar" para atualizar os dados

### 3. Exportar Dados

#### PDF:
1. Clique no botão "Exportar PDF"
2. O arquivo será baixado automaticamente
3. Nome do arquivo: `relatorio-{tipo}.pdf`

#### Excel:
1. Clique no botão "Exportar Excel"
2. O arquivo será baixado automaticamente
3. Nome do arquivo: `relatorio-{tipo}.xlsx`

#### Imprimir:
1. Clique no botão "Imprimir"
2. Janela de impressão será aberta
3. Selecione impressora ou salvar como PDF

---

## 📊 Exemplos de Dados nos Relatórios

### Relatório de Candidatos por Vaga
```
📌 Vaga: Monitor de Programação I
   Curso: Análise e Desenvolvimento de Sistemas
   Vagas: 2 | Inscritos: 15

┌────┬──────────────────┬────────┬─────┬────────────┬────────────┬──────┬────────────┐
│  # │ Candidato        │ Curso  │ CR  │ Data Insc. │ Status     │ Nota │ Documentos │
├────┼──────────────────┼────────┼─────┼────────────┼────────────┼──────┼────────────┤
│  1 │ João Silva       │ ADS    │ 8.5 │ 15/01/2025 │ Aprovado   │ 9/10 │ 3 doc(s)   │
│  2 │ Maria Santos     │ ADS    │ 8.2 │ 16/01/2025 │ Aprovado   │ 8/10 │ 3 doc(s)   │
│  3 │ Pedro Oliveira   │ ADS    │ 7.9 │ 17/01/2025 │ Pendente   │  -   │ 2 doc(s)   │
└────┴──────────────────┴────────┴─────┴────────────┴────────────┴──────┴────────────┘
```

### Relatório de Monitores Selecionados
```
📊 Estatísticas Gerais
   ✓ Total de Monitores: 45
   ✓ Vagas Preenchidas: 42
   ✓ Média CR: 8.3
   ✓ Disciplinas: 18

📈 Distribuição por Curso:
   • Análise e Desenvolvimento de Sistemas: 18 monitores
   • Engenharia de Software: 15 monitores
   • Redes de Computadores: 12 monitores
```

### Relatório de Horas Trabalhadas
```
💰 Resumo Financeiro
   ⏱️ Total de Horas: 1,245.5h
   💵 Valor Total: R$ 24,910.00
   ⏳ Horas Pendentes: 123.0h
   👥 Monitores Ativos: 45

📊 Resumo por Monitor:
┌──────────────────┬──────────┬──────────────┬────────────────┬──────────────┐
│ Monitor          │ Registros│ H. Aprovadas │ H. Pendentes   │ Valor Total  │
├──────────────────┼──────────┼──────────────┼────────────────┼──────────────┤
│ João Silva       │    12    │    45.5h     │     4.0h       │  R$ 910.00   │
│ Maria Santos     │    10    │    38.0h     │     2.5h       │  R$ 760.00   │
└──────────────────┴──────────┴──────────────┴────────────────┴──────────────┘
```

---

## 🎯 Próximos Passos Sugeridos

### 1. Integração Power BI
- Substituir Chart.js por Power BI Embedded
- Criar workspace no Power BI
- Configurar autenticação Azure AD
- Incorporar relatórios interativos

### 2. Melhorias de Exportação
- **PDF Avançado:**
  - Gráficos incluídos no PDF
  - Cabeçalho/rodapé personalizados
  - Marca d'água institucional
  
- **Excel Avançado:**
  - Formatação condicional
  - Tabelas dinâmicas
  - Fórmulas automáticas

### 3. Automação de Relatórios
- Agendamento de geração
- Envio automático por email
- Relatórios periódicos (semanal/mensal)

### 4. API REST
- Endpoints para dados de relatórios
- Autenticação JWT
- Versionamento de API

---

## ✅ Checklist de Implementação

- [x] Templates de relatórios criados (3)
- [x] Views atualizadas com dados completos
- [x] Exportação PDF implementada
- [x] Exportação Excel implementada
- [x] Funcionalidade de impressão
- [x] Gráficos Chart.js integrados
- [x] Filtros avançados funcionando
- [x] Estatísticas calculadas
- [x] Interface responsiva
- [x] Documentação completa

---

## 📚 Referências

- **jsPDF:** https://github.com/parallax/jsPDF
- **jsPDF-AutoTable:** https://github.com/simonbengtsson/jsPDF-AutoTable
- **SheetJS:** https://sheetjs.com/
- **Chart.js:** https://www.chartjs.org/
- **Bootstrap 5:** https://getbootstrap.com/
- **Font Awesome:** https://fontawesome.com/

---

**Data de Implementação:** 24/01/2025  
**Versão:** 1.0  
**Desenvolvedor:** Anderson  
**Projeto:** Sistema de Monitoria - PBE 25.2

