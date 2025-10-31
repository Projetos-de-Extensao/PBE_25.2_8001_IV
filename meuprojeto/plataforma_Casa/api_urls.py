from rest_framework.routers import DefaultRouter

from .api.viewsets import (
    TipoUsuarioViewSet,
    CursoViewSet,
    SalaViewSet,
    DisciplinaViewSet,
    UsuarioViewSet,
    FuncionarioViewSet,
    AlunoViewSet,
    VagaViewSet,
    TurmaViewSet,
    ParticipacaoMonitoriaViewSet,
    PresencaViewSet,
    InscricaoViewSet,
    DocumentoViewSet,
    RegistroHorasViewSet,
    StatusPagamentoViewSet,
    MaterialApoioViewSet,
    EstatisticasViewSet,
)

# ============================================================================
# ROUTER DA API REST - TODOS OS ENDPOINTS
# ============================================================================
# Router padrão do DRF que gera automaticamente as URLs para os ViewSets
# Cada ViewSet registrado aqui terá endpoints completos de CRUD e ações customizadas

router = DefaultRouter()

# ---------- ENDPOINTS BASE ----------
# Gerenciamento de tipos de usuário, cursos, salas e disciplinas
router.register(r'tipos-usuario', TipoUsuarioViewSet, basename='tipo-usuario')
router.register(r'cursos', CursoViewSet, basename='curso')
router.register(r'salas', SalaViewSet, basename='sala')
router.register(r'disciplinas', DisciplinaViewSet, basename='disciplina')

# ---------- ENDPOINTS DE USUÁRIOS ----------
# Gerenciamento de usuários, funcionários e alunos
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'funcionarios', FuncionarioViewSet, basename='funcionario')
router.register(r'alunos', AlunoViewSet, basename='aluno')

# ---------- ENDPOINTS DE VAGAS E TURMAS ----------
# Gerenciamento de vagas de monitoria e turmas
router.register(r'vagas', VagaViewSet, basename='vaga')
router.register(r'turmas', TurmaViewSet, basename='turma')

# ---------- ENDPOINTS DE PARTICIPAÇÃO E PRESENÇA ----------
# Gerenciamento de participações em monitorias e registro de presenças
router.register(r'participacoes', ParticipacaoMonitoriaViewSet, basename='participacao')
router.register(r'presencas', PresencaViewSet, basename='presenca')

# ---------- ENDPOINTS DE INSCRIÇÕES E DOCUMENTOS ----------
# Gerenciamento de inscrições em vagas e documentos anexados
router.register(r'inscricoes', InscricaoViewSet, basename='inscricao')
router.register(r'documentos', DocumentoViewSet, basename='documento')

# ---------- ENDPOINTS DE HORAS E PAGAMENTOS ----------
# Gerenciamento de registro de horas trabalhadas e pagamentos
router.register(r'registro-horas', RegistroHorasViewSet, basename='registro-horas')
router.register(r'pagamentos', StatusPagamentoViewSet, basename='pagamento')

# ---------- ENDPOINTS DE MATERIAIS ----------
# Gerenciamento de materiais de apoio para as turmas
router.register(r'materiais', MaterialApoioViewSet, basename='material')

# ---------- ENDPOINTS DE ESTATÍSTICAS ----------
# Endpoints para consultar estatísticas do sistema
router.register(r'estatisticas', EstatisticasViewSet, basename='estatisticas')

# URLs geradas automaticamente pelo router
urlpatterns = router.urls

# ============================================================================
# ENDPOINTS DISPONÍVEIS
# ============================================================================
# 
# BASE:
# - GET    /api/tipos-usuario/                    Lista todos os tipos de usuário
# - POST   /api/tipos-usuario/                    Cria novo tipo de usuário
# - GET    /api/tipos-usuario/{id}/               Detalhes de um tipo
# - PUT    /api/tipos-usuario/{id}/               Atualiza um tipo
# - PATCH  /api/tipos-usuario/{id}/               Atualiza parcialmente
# - DELETE /api/tipos-usuario/{id}/               Remove um tipo
# - GET    /api/tipos-usuario/ativos/             Lista apenas ativos
#
# - GET    /api/cursos/                           Lista todos os cursos
# - POST   /api/cursos/                           Cria novo curso
# - GET    /api/cursos/{id}/                      Detalhes de um curso
# - PUT    /api/cursos/{id}/                      Atualiza um curso
# - PATCH  /api/cursos/{id}/                      Atualiza parcialmente
# - DELETE /api/cursos/{id}/                      Remove um curso
# - GET    /api/cursos/ativos/                    Lista apenas ativos
# - GET    /api/cursos/{id}/estatisticas/         Estatísticas do curso
#
# - GET    /api/salas/                            Lista todas as salas
# - POST   /api/salas/                            Cria nova sala
# - GET    /api/salas/{id}/                       Detalhes de uma sala
# - PUT    /api/salas/{id}/                       Atualiza uma sala
# - PATCH  /api/salas/{id}/                       Atualiza parcialmente
# - DELETE /api/salas/{id}/                       Remove uma sala
# - GET    /api/salas/disponiveis/                Lista apenas disponíveis
#
# USUÁRIOS:
# - GET    /api/usuarios/                         Lista todos os usuários
# - POST   /api/usuarios/                         Cria novo usuário
# - GET    /api/usuarios/{id}/                    Detalhes de um usuário
# - PUT    /api/usuarios/{id}/                    Atualiza um usuário
# - PATCH  /api/usuarios/{id}/                    Atualiza parcialmente
# - DELETE /api/usuarios/{id}/                    Remove um usuário
#
# - GET    /api/funcionarios/                     Lista todos os funcionários
# - POST   /api/funcionarios/                     Cria novo funcionário
# - GET    /api/funcionarios/{id}/                Detalhes de um funcionário
# - PUT    /api/funcionarios/{id}/                Atualiza um funcionário
# - PATCH  /api/funcionarios/{id}/                Atualiza parcialmente
# - DELETE /api/funcionarios/{id}/                Remove um funcionário
# - GET    /api/funcionarios/coordenadores/       Lista apenas coordenadores
# - GET    /api/funcionarios/por_departamento/    Lista por departamento
#
# - GET    /api/alunos/                           Lista todos os alunos
# - POST   /api/alunos/                           Cria novo aluno
# - GET    /api/alunos/{id}/                      Detalhes de um aluno
# - PUT    /api/alunos/{id}/                      Atualiza um aluno
# - PATCH  /api/alunos/{id}/                      Atualiza parcialmente
# - DELETE /api/alunos/{id}/                      Remove um aluno
# - GET    /api/alunos/por_curso/                 Lista alunos de um curso
# - GET    /api/alunos/por_periodo/               Lista alunos de um período
# - GET    /api/alunos/monitores/                 Lista alunos monitores
# - GET    /api/alunos/{id}/desempenho/           Desempenho do aluno
#
# VAGAS E TURMAS:
# - GET    /api/vagas/                            Lista todas as vagas
# - POST   /api/vagas/                            Cria nova vaga
# - GET    /api/vagas/{id}/                       Detalhes de uma vaga
# - PUT    /api/vagas/{id}/                       Atualiza uma vaga
# - PATCH  /api/vagas/{id}/                       Atualiza parcialmente
# - DELETE /api/vagas/{id}/                       Remove uma vaga
# - GET    /api/vagas/ativas/                     Lista vagas ativas
# - GET    /api/vagas/por_curso/                  Lista vagas de um curso
# - GET    /api/vagas/com_vagas_disponiveis/      Lista vagas disponíveis
# - GET    /api/vagas/{id}/inscricoes/            Inscrições da vaga
#
# - GET    /api/turmas/                           Lista todas as turmas
# - POST   /api/turmas/                           Cria nova turma
# - GET    /api/turmas/{id}/                      Detalhes de uma turma
# - PUT    /api/turmas/{id}/                      Atualiza uma turma
# - PATCH  /api/turmas/{id}/                      Atualiza parcialmente
# - DELETE /api/turmas/{id}/                      Remove uma turma
# - GET    /api/turmas/ativas/                    Lista turmas ativas
# - GET    /api/turmas/por_monitor/               Lista turmas de um monitor
# - GET    /api/turmas/por_periodo/               Lista turmas no período
# - GET    /api/turmas/{id}/participantes/        Participantes da turma
# - GET    /api/turmas/{id}/presencas/            Presenças da turma
# - GET    /api/turmas/{id}/materiais/            Materiais da turma
#
# PARTICIPAÇÃO E PRESENÇA:
# - GET    /api/participacoes/                    Lista todas as participações
# - POST   /api/participacoes/                    Registra participação
# - GET    /api/participacoes/{id}/               Detalhes de uma participação
# - PUT    /api/participacoes/{id}/               Atualiza participação
# - PATCH  /api/participacoes/{id}/               Atualiza parcialmente
# - DELETE /api/participacoes/{id}/               Remove participação
# - GET    /api/participacoes/por_aluno/          Participações de um aluno
# - GET    /api/participacoes/por_turma/          Participações de uma turma
#
# - GET    /api/presencas/                        Lista todas as presenças
# - POST   /api/presencas/                        Registra presença
# - GET    /api/presencas/{id}/                   Detalhes de uma presença
# - PUT    /api/presencas/{id}/                   Atualiza presença
# - PATCH  /api/presencas/{id}/                   Atualiza parcialmente
# - DELETE /api/presencas/{id}/                   Remove presença
# - GET    /api/presencas/por_aluno/              Presenças de um aluno
# - GET    /api/presencas/por_turma/              Presenças de uma turma
# - GET    /api/presencas/por_data/               Presenças em uma data
# - GET    /api/presencas/taxa_presenca/          Taxa de presença
#
# INSCRIÇÕES E DOCUMENTOS:
# - GET    /api/inscricoes/                       Lista todas as inscrições
# - POST   /api/inscricoes/                       Cria inscrição
# - GET    /api/inscricoes/{id}/                  Detalhes de uma inscrição
# - PUT    /api/inscricoes/{id}/                  Atualiza inscrição
# - PATCH  /api/inscricoes/{id}/                  Atualiza parcialmente
# - DELETE /api/inscricoes/{id}/                  Remove inscrição
# - GET    /api/inscricoes/por_status/            Lista por status
# - GET    /api/inscricoes/por_aluno/             Inscrições de um aluno
# - GET    /api/inscricoes/por_vaga/              Inscrições de uma vaga
# - POST   /api/inscricoes/{id}/aprovar/          Aprova inscrição
# - POST   /api/inscricoes/{id}/rejeitar/         Rejeita inscrição
#
# - GET    /api/documentos/                       Lista todos os documentos
# - POST   /api/documentos/                       Upload de documento
# - GET    /api/documentos/{id}/                  Detalhes de um documento
# - PUT    /api/documentos/{id}/                  Atualiza documento
# - PATCH  /api/documentos/{id}/                  Atualiza parcialmente
# - DELETE /api/documentos/{id}/                  Remove documento
# - GET    /api/documentos/por_inscricao/         Documentos de uma inscrição
# - GET    /api/documentos/por_tipo/              Documentos por tipo
#
# HORAS E PAGAMENTOS:
# - GET    /api/registro-horas/                   Lista todos os registros
# - POST   /api/registro-horas/                   Cria registro de horas
# - GET    /api/registro-horas/{id}/              Detalhes de um registro
# - PUT    /api/registro-horas/{id}/              Atualiza registro
# - PATCH  /api/registro-horas/{id}/              Atualiza parcialmente
# - DELETE /api/registro-horas/{id}/              Remove registro
# - GET    /api/registro-horas/por_monitor/       Registros de um monitor
# - GET    /api/registro-horas/por_turma/         Registros de uma turma
# - GET    /api/registro-horas/por_status/        Registros por status
# - GET    /api/registro-horas/pendentes/         Registros pendentes
# - POST   /api/registro-horas/{id}/aprovar/      Aprova registro
# - POST   /api/registro-horas/{id}/rejeitar/     Rejeita registro
# - GET    /api/registro-horas/total_horas_monitor/ Total de horas
#
# - GET    /api/pagamentos/                       Lista todos os pagamentos
# - POST   /api/pagamentos/                       Cria pagamento
# - GET    /api/pagamentos/{id}/                  Detalhes de um pagamento
# - PUT    /api/pagamentos/{id}/                  Atualiza pagamento
# - PATCH  /api/pagamentos/{id}/                  Atualiza parcialmente
# - DELETE /api/pagamentos/{id}/                  Remove pagamento
# - GET    /api/pagamentos/por_monitor/           Pagamentos de um monitor
# - GET    /api/pagamentos/por_status/            Pagamentos por status
# - GET    /api/pagamentos/pendentes/             Pagamentos pendentes
# - POST   /api/pagamentos/{id}/processar/        Processa pagamento
#
# MATERIAIS:
# - GET    /api/materiais/                        Lista todos os materiais
# - POST   /api/materiais/                        Upload de material
# - GET    /api/materiais/{id}/                   Detalhes de um material
# - PUT    /api/materiais/{id}/                   Atualiza material
# - PATCH  /api/materiais/{id}/                   Atualiza parcialmente
# - DELETE /api/materiais/{id}/                   Remove material
# - GET    /api/materiais/por_turma/              Materiais de uma turma
# - GET    /api/materiais/por_tipo/               Materiais por tipo
# - GET    /api/materiais/publicados/             Materiais publicados
#
# ESTATÍSTICAS:
# - GET    /api/estatisticas/geral/               Estatísticas gerais
#
# ============================================================================
