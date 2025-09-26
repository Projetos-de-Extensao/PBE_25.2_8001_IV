# Documentação da Arquitetura - Sistema de Gestão de Monitoria

Este diretório contém a documentação completa da arquitetura do sistema, incluindo diagramas PlantUML e especificações técnicas.

## 📋 Índice

### 🏗️ Diagramas de Arquitetura
- [Visão Geral do Sistema](./01-visao-geral-sistema.puml) - Arquitetura de alto nível
- [Arquitetura de Componentes](./02-arquitetura-componentes.puml) - Componentes detalhados
- [Diagrama de Implantação](./03-diagrama-implantacao.puml) - Infraestrutura e deploy

### 🔄 Diagramas de Processo
- [Fluxo de Autenticação](./04-fluxo-autenticacao.puml) - Processo de login/logout
- [Fluxo de Monitoria](./05-fluxo-monitoria.puml) - Processo de gestão de monitorias
- [Fluxo de Relatórios](./06-fluxo-relatorios.puml) - Geração de relatórios

### 🗄️ Diagramas de Dados
- [Modelo de Dados](./07-modelo-dados.puml) - Estrutura do banco de dados
- [Diagrama de Classes](./08-diagrama-classes.puml) - Classes do backend Django
- [Componentes React](./09-componentes-react.puml) - Estrutura frontend

### 🌐 Diagramas de API
- [Endpoints da API](./10-endpoints-api.puml) - Mapeamento completo da API REST
- [Sequência de Requisições](./11-sequencia-requisicoes.puml) - Fluxo de dados

### 🛡️ Diagramas de Segurança
- [Modelo de Segurança](./12-modelo-seguranca.puml) - Autenticação e autorização

## 🛠️ Tecnologias

### Backend
- **Django**: Framework web Python
- **Django REST Framework**: Para criação da API REST
- **PostgreSQL**: Banco de dados principal
- **sqlite**: Banco de dados para testes
- **Redis**: Cache e sessões
- **Celery**: Processamento assíncrono

### Frontend
- **React**: Biblioteca JavaScript para UI
- **TypeScript**: Para tipagem estática
- **Material-UI**: Componentes de interface
- **Axios**: Cliente HTTP para API

### DevOps
- **Docker**: Containerização
- **Nginx**: Servidor web e proxy reverso
- **GitHub Actions**: CI/CD
- **AWS**: Infraestrutura cloud

## 📚 Como usar os diagramas

Os diagramas estão em formato PlantUML e podem ser visualizados:

1. **Online**: [PlantText](https://www.planttext.com/)
2. **VS Code**: Extensão PlantUML
3. **CLI**: `plantuml arquivo.puml`

## 🔄 Atualizações

Esta documentação deve ser atualizada sempre que houver mudanças na arquitetura do sistema.

Última atualização: Setembro 2025