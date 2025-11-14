# Analisador de Histórico Acadêmico

## 📋 Descrição

O `AnalisadorHistorico` é uma classe responsável por analisar documentos PDF de histórico escolar para validar automaticamente candidaturas a vagas de monitoria.

## 🎯 Funcionalidades

- ✅ Extração de dados de histórico acadêmico em PDF
- ✅ Validação de matrícula do aluno
- ✅ Verificação de carga horária cursada (mínimo: 800h)
- ✅ Análise do CR específico na disciplina (mínimo: 8.0)
- ✅ Cálculo e validação do CR geral (mínimo: 7.0)
- ✅ Decisão automática de aprovação/rejeição

## 📦 Dependências

```bash
pip install pdfplumber==0.11.4
```

Ou usando o requirements.txt do projeto:

```bash
pip install -r requirements.txt
```

## 💻 Como Usar

### Exemplo Básico

```python
from plataforma_Casa.analisador_historico import AnalisadorHistorico
from plataforma_Casa.models import Vaga, Aluno

# Obter a vaga e o aluno
vaga = Vaga.objects.get(id=1)
aluno = Aluno.objects.get(matricula="202012345")

# Criar instância do analisador
analisador = AnalisadorHistorico(vaga_recebida=vaga, aluno_recebido=aluno)

# Analisar o PDF do histórico
caminho_pdf = "/caminho/para/historico.pdf"
resultado = analisador.analisar_e_decidir(caminho_pdf)

print(f"Resultado da análise: {resultado}")
# Possíveis resultados:
# - "CANDIDATURA APROVADA" - Aluno atende todos os requisitos
# - "REJEITADO" - Aluno não atende os requisitos mínimos
# - "PENDENTE" - PDF ilegível ou sem dados suficientes
```

### Integração com Views

```python
from django.shortcuts import render, redirect
from django.contrib import messages
from .analisador_historico import AnalisadorHistorico
from .models import Inscricao, Vaga, Aluno

def processar_inscricao(request, vaga_id):
    if request.method == 'POST':
        vaga = Vaga.objects.get(id=vaga_id)
        aluno = request.user.aluno
        
        # Upload do histórico
        arquivo_historico = request.FILES.get('historico_pdf')
        
        if arquivo_historico:
            # Salvar o arquivo temporariamente
            caminho_temp = f'/tmp/historico_{aluno.matricula}.pdf'
            with open(caminho_temp, 'wb+') as destination:
                for chunk in arquivo_historico.chunks():
                    destination.write(chunk)
            
            # Analisar o histórico
            analisador = AnalisadorHistorico(vaga, aluno)
            resultado = analisador.analisar_e_decidir(caminho_temp)
            
            # Criar inscrição com o status automatizado
            inscricao = Inscricao.objects.create(
                aluno=aluno,
                vaga=vaga,
                status=resultado,
                historico_pdf=arquivo_historico
            )
            
            if resultado == "CANDIDATURA APROVADA":
                messages.success(request, 'Sua candidatura foi APROVADA automaticamente!')
            elif resultado == "REJEITADO":
                messages.error(request, 'Sua candidatura foi rejeitada. Você não atende aos requisitos mínimos.')
            else:
                messages.info(request, 'Sua candidatura está pendente de análise manual.')
            
            return redirect('minhas_inscricoes')
    
    return render(request, 'inscricoes/candidatar.html')
```

## 🔍 Critérios de Validação

O analisador verifica os seguintes critérios:

| Critério | Valor Mínimo | Descrição |
|----------|--------------|-----------|
| **Carga Horária** | 800.0 horas | Total de horas cursadas no curso |
| **CR Específico** | 8.0 | Nota na disciplina específica da vaga |
| **CR Geral** | 7.0 | Média geral de todos os períodos |
| **Matrícula** | - | Deve corresponder à matrícula do aluno |

## 📝 Estrutura do PDF Esperada

O analisador espera que o PDF do histórico contenha:

1. **Cabeçalho** com:
   - Label "Matrícula:" seguido do número de matrícula

2. **Tabelas de notas** contendo:
   - Coluna com "Carga Horária Total"
   - Linha com o nome da disciplina específica
   - Coluna com "C.R. do Período:"
   - Valores numéricos nas posições corretas

## ⚙️ Configuração Personalizada

Para ajustar os critérios mínimos, edite o dicionário `config` no método `__init__`:

```python
self.config = {
    "horas_cursadas": {
        "keyword": "Carga Horária Total",
        "index": 2,
        "valor": 0,
        "valor_min": 800.0,  # Altere aqui
    },
    "cr_especifico": {
        "keyword": self.vaga_alvo,
        "index": 7,
        "valor": 0,
        "valor_min": 8.0,  # Altere aqui
    },
    "cr_geral": {
        "valor": 0.0, 
        "valor_min": 7.0  # Altere aqui
    },
}
```

## 🐛 Debug e Logs

O analisador imprime logs detalhados durante a execução:

```python
# Exemplo de saída no console:
Iniciando análise do PDF: /path/to/historico.pdf
INFO: Matrícula 202012345 encontrada no cabeçalho.
Procurando Matrícula: 202012345
Matrícula Encontrada no PDF: True
Horas: 920.0 (Min: 800.0)
CR Específico: 8.5 (Min: 8.0)
CR Geral: 7.8 (Min: 7.0)
Resultado: CANDIDATURA APROVADA (automaticamente)
```

## ⚠️ Tratamento de Erros

O analisador retorna `"PENDENTE"` nos seguintes casos:

- PDF ilegível ou corrompido
- PDF sem texto extraível
- PDF sem tabelas de notas
- Erros durante a leitura do arquivo

Nesses casos, a candidatura deve ser analisada manualmente.

## 🔧 Manutenção

### Ajustar índices das colunas

Se a estrutura do PDF mudar, ajuste os índices no `config`:

```python
"cr_especifico": {
    "keyword": self.vaga_alvo,
    "index": 7,  # Índice da coluna com a nota
    ...
}
```

### Adicionar novos critérios

Para adicionar um novo critério de validação:

1. Adicione ao `config` no `__init__`
2. Extraia os dados em `extrair_dados_tabelas`
3. Valide em `candidato_apto`

## 📚 Referências

- [pdfplumber Documentation](https://github.com/jsvine/pdfplumber)
- [Django File Uploads](https://docs.djangoproject.com/en/5.0/topics/http/file-uploads/)

## 📄 Licença

Este código faz parte do sistema de monitoria PBE_25.2_8001_IV.
