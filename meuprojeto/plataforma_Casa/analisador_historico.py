"""
Analisador de Histórico Acadêmico
Responsável por analisar documentos PDF de histórico escolar
para validar candidaturas a vagas de monitoria automaticamente.
"""

import pdfplumber
from .models import Vaga, Aluno
from django.contrib.auth.models import User
import re


class AnalisadorHistorico:
    """
    Classe responsável por analisar históricos acadêmicos em PDF
    e determinar se um aluno atende aos requisitos para monitoria.
    """

    def __init__(self, vaga_recebida: Vaga, aluno_recebido: Aluno):
        """
        Inicializa o analisador com a vaga e o aluno.
        
        Args:
            vaga_recebida: Vaga de monitoria para a qual o aluno está se candidatando
            aluno_recebido: Aluno que está se candidatando
        """
        self.vaga_alvo = vaga_recebida.disciplina.nome.upper()
        self.matricula_alvo = aluno_recebido.matricula
        self.matricula_encontrada_no_pdf = False

        self.config = {
            "horas_cursadas": {
                "keyword": "Carga Horária Total",
                "index": 2,
                "valor": 0,
                "valor_min": 800.0,
            },
            "cr_especifico": {
                "keyword": self.vaga_alvo,
                "index": 7,
                "valor": 0,
                "valor_min": 8.0,
            },
            "cr_periodo_soma": {
                "keyword": "C.R. do Período:",
                "index": 8,
                "valor": 0,
                "count": 0,
            },
            "cr_geral": {"valor": 0.0, "valor_min": 7.0},
        }

    def ler_tabelas_academicas(self, url_pdf):
        """
        Extrai todas as tabelas de notas do PDF.
        
        Args:
            url_pdf: Caminho ou URL do arquivo PDF
            
        Returns:
            Lista de tabelas extraídas do PDF
        """
        try:
            with pdfplumber.open(url_pdf) as pdf:
                tabelas = []
                for page in pdf.pages:
                    tabelas_pagina = page.extract_tables()
                    if tabelas_pagina:
                        tabelas.extend(tabelas_pagina[1:]) 
                
                if not tabelas:
                    print(f"AVISO: Nenhuma tabela de NOTAS encontrada no PDF: {url_pdf}")
                    return []
                return tabelas
        except Exception as e:
            print(f"ERRO ao ler tabelas do PDF: {e}")
            return []

    def ler_texto_cabecalho(self, url_pdf):
        """
        Extrai o texto do cabeçalho (primeira página) do PDF.
        
        Args:
            url_pdf: Caminho ou URL do arquivo PDF
            
        Returns:
            Texto extraído do cabeçalho ou None em caso de erro
        """
        try:
            with pdfplumber.open(url_pdf) as pdf:
                primeira_pagina = pdf.pages[0]
                return primeira_pagina.extract_text()
        except Exception as e:
            print(f"ERRO ao extrair texto do PDF: {e}")
            return None

    def verificar_matricula_pdf(self, texto_cabecalho: str):
        """
        Verifica se a matrícula do aluno está presente no cabeçalho do PDF.
        
        Args:
            texto_cabecalho: Texto extraído do cabeçalho do PDF
        """
        keyword_label = "Matrícula:"
        
        if not texto_cabecalho:
            print("AVISO: Não foi possível ler o texto do cabeçalho.")
            return 

        if keyword_label in texto_cabecalho:
            numeros_no_texto = "".join(re.findall(r'\d+', texto_cabecalho))
    
            if self.matricula_alvo in numeros_no_texto:
                self.matricula_encontrada_no_pdf = True
                print(f"INFO: Matrícula {self.matricula_alvo} encontrada no cabeçalho.")
                return
        
        print(f"AVISO: Matrícula {self.matricula_alvo} NÃO encontrada no cabeçalho.")
        self.matricula_encontrada_no_pdf = False
    
    @staticmethod
    def tratar_valor(elemento):
        """
        Converte um elemento de texto em valor numérico float.
        
        Args:
            elemento: String contendo o valor a ser convertido
            
        Returns:
            Valor float ou 0.0 em caso de erro
        """
        if elemento is None:
            return 0.0
        try:
            return float(elemento.strip().replace(",", "."))
        except (ValueError, TypeError):
            return 0.0

    def procura_keyword(self, linha: list, mapa: dict) -> bool:
        """
        Verifica se uma keyword está presente em uma linha da tabela.
        
        Args:
            linha: Lista de elementos da linha
            mapa: Dicionário com configuração incluindo a keyword
            
        Returns:
            True se a keyword foi encontrada, False caso contrário
        """
        if not mapa.get("keyword"): 
            return False
        linha_texto = " ".join(filter(None, linha))
        if mapa["keyword"] in linha_texto:
            return True
        return False

    def extrair_dados_linha(self, linha, mapa, adicionar=False):
        """
        Extrai dados de uma linha da tabela baseado na configuração do mapa.
        
        Args:
            linha: Lista de elementos da linha
            mapa: Dicionário com configuração de extração
            adicionar: Se True, soma o valor; se False, substitui
        """
        possui_keyword = self.procura_keyword(linha, mapa)

        if possui_keyword:
            elemento_tratado = self.tratar_valor(linha[mapa["index"]])
            if adicionar:
                mapa["valor"] += elemento_tratado
                mapa["count"] += 1
            else:
                mapa["valor"] = elemento_tratado
        else:
            return

    def extrair_cr_geral(self):
        """
        Calcula o CR geral como média dos CRs de período.
        """
        cr_periodo_soma = self.config["cr_periodo_soma"]
        cr_geral = self.config["cr_geral"]

        if cr_periodo_soma["count"] > 0:
            cr_geral["valor"] = cr_periodo_soma["valor"] / cr_periodo_soma["count"]
        else:
            cr_geral["valor"] = 0.0

    def extrair_dados_tabelas(self, tabelas_academicas: list):
        """
        Processa todas as tabelas extraídas do PDF para coletar dados acadêmicos.
        
        Args:
            tabelas_academicas: Lista de tabelas extraídas do PDF
        """
        if not tabelas_academicas: 
            return

        for tabela in tabelas_academicas:
            for linha in tabela:
                self.extrair_dados_linha(linha, self.config["horas_cursadas"])
                self.extrair_dados_linha(linha, self.config["cr_especifico"])
                self.extrair_dados_linha(linha, self.config["cr_periodo_soma"], True)
        
        self.extrair_cr_geral()

    @staticmethod
    def valor_suficiente(mapa):
        """
        Verifica se o valor atingido é suficiente comparado ao mínimo exigido.
        
        Args:
            mapa: Dicionário contendo 'valor' e 'valor_min'
            
        Returns:
            True se o valor é suficiente, False caso contrário
        """
        if mapa["valor"] >= mapa["valor_min"]:
            return True
        return False
    
    def candidato_apto(self):
        """
        Verifica se o candidato atende a todos os requisitos para monitoria.
        
        Returns:
            True se o candidato está apto, False caso contrário
        """
        horas_cursadas = self.config["horas_cursadas"]
        cr_especifico = self.config["cr_especifico"]
        cr_geral = self.config["cr_geral"]

        matricula_valida = self.matricula_encontrada_no_pdf

        print(f"Procurando Matrícula: {self.matricula_alvo}")
        print(f"Matrícula Encontrada no PDF: {matricula_valida}")
        print(f"Horas: {horas_cursadas['valor']} (Min: {horas_cursadas['valor_min']})")
        print(f"CR Específico: {cr_especifico['valor']} (Min: {cr_especifico['valor_min']})")
        print(f"CR Geral: {cr_geral['valor']} (Min: {cr_geral['valor_min']})")

        if not matricula_valida:
            print("Validação falhou: Matrícula não encontrada ou não compatível.")
            return False

        return (
            self.valor_suficiente(horas_cursadas)
            and self.valor_suficiente(cr_especifico)
            and self.valor_suficiente(cr_geral)
        )
    
    def analisar_e_decidir(self, url_pdf: str) -> str:
        """
        Método principal que executa toda a análise do histórico.
        
        Args:
            url_pdf: Caminho ou URL do arquivo PDF do histórico
            
        Returns:
            String com o resultado: "CANDIDATURA APROVADA", "REJEITADO" ou "PENDENTE"
        """
        print(f"Iniciando análise do PDF: {url_pdf}")
        
        texto_cabecalho = self.ler_texto_cabecalho(url_pdf)
        if not texto_cabecalho:
            print("Análise falhou: PDF sem texto ou ilegível.")
            return "PENDENTE" 
        
        tabelas_notas = self.ler_tabelas_academicas(url_pdf)
        if not tabelas_notas:
            print("Análise falhou: PDF sem tabelas de notas.")
            return "PENDENTE" 

        self.verificar_matricula_pdf(texto_cabecalho)
        self.extrair_dados_tabelas(tabelas_notas)
        
        if self.candidato_apto():
            print("Resultado: CANDIDATURA APROVADA (automaticamente)")
            return "CANDIDATURA APROVADA"
        else:
            print("Resultado: REJEITADO (critérios não atingidos ou matrícula inválida)")
            return "REJEITADO"
