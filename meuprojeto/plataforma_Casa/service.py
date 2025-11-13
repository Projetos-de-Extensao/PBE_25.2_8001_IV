import json
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from django.db import IntegrityError, transaction

from .repository import (
    AlunoRepository,
    AuthRepository,
    DashboardGestaoRepository,
    DisciplinaRepository,
    MonitoriaRepository,
    PerfilRepository,
    PortalVagasRepository,
    PresencaRepository,
    RegistroHorasRepository,
    RegistroRepository,
    RelatorioRepository,
    TurmaRepository,
    UsuarioRepository,
    VagaRepository

)

from .models import (
    Curso,
    ParticipacaoMonitoria, 
    Presenca, 
    Inscricao,
    Sala,
    TipoUsuario, 
    Usuario, 
    Aluno, 
    Funcionario, 
    Turma, 
    Vaga
)

class BaseService:
    @staticmethod
    def safe_count(qs):
        try:
            return qs.count()
        except Exception:
            return 0

class VagaService(BaseService):
    def __init__(self, vaga_id, user):
        self.vaga = VagaRepository.get_vaga_by_id(vaga_id)
        self.user = user

    def check_permission(self):
        if self.user.is_staff or self.user.is_superuser:
            return True

        try:
            funcionario = VagaRepository.get_funcionario_by_email(self.user.email)
        except Funcionario.DoesNotExist:
            raise PermissionDenied("Professor não encontrado")

        if funcionario in VagaRepository.get_coordenadores(self.vaga) or funcionario in VagaRepository.get_professores(self.vaga):
            return True

        raise PermissionDenied("Você não tem permissão para ver esta vaga")

    def get_inscricoes_qs(self):
        return VagaRepository.get_inscricoes_by_vaga(self.vaga)

    def get_stats(self):
        qs = self.get_inscricoes_qs()
        return {
            'total_inscricoes': self.safe_count(qs),
            'pendentes': qs.filter(status='Pendente').count(),
            'entrevista': qs.filter(status='Entrevista').count(),
            'aprovados': qs.filter(status='Aprovado').count(),
            'rejeitados': qs.filter(status='Não Aprovado').count(),
        }

    def vaga_service(self):
        self.check_permission()
        inscricoes = self.get_inscricoes_qs()
        stats = self.get_stats()
        context = {
            'vaga': self.vaga,
            'inscricoes': inscricoes,
            **stats
        }
        return context


class UsuarioService:
    """Service para operações CRUD simples sobre Usuario."""

    def list_users(self, tipo_id=None, ativo=None):
        return UsuarioRepository.list_users(tipo_id, ativo)

    def create_user(self, nome, email, tipo_usuario_id):
        tipo = UsuarioRepository.get_tipo_usuario_by_id(tipo_usuario_id)
        try:
            usuario = UsuarioRepository.create_usuario(nome, email, tipo)
            return usuario
        except IntegrityError as e:
            raise

    def update_user(self, usuario_id, nome=None, email=None, ativo=None):
        usuario = UsuarioRepository.get_usuario_by_id(usuario_id)
        if nome is not None:
            usuario.nome = nome
        if email is not None:
            usuario.email = email
        if ativo is not None:
            usuario.ativo = ativo
        usuario.save()
        return usuario

    def delete_user(self, usuario_id):
        usuario = UsuarioRepository.get_usuario_by_id(usuario_id)
        nome = usuario.nome
        usuario.delete()
        return nome
    


class AlunoService:
    """Service para operações CRUD de Aluno."""

    def list_alunos(self, curso_id=None, periodo=None):
        return AlunoRepository.list_alunos(curso_id, periodo)

    def create_aluno(self, nome, email, matricula, curso_id, periodo=None, cr_geral=0.0):
        curso = AlunoRepository.get_curso_by_id(curso_id)
        tipo_usuario, _ = AlunoRepository.get_or_create_tipo_usuario_aluno()

        try:
            periodo_val = int(periodo) if periodo is not None and periodo != '' else None
        except (ValueError, TypeError):
            periodo_val = None

        try:
            cr_val = float(cr_geral) if cr_geral not in (None, '') else 0.0
        except (ValueError, TypeError):
            cr_val = 0.0

        try:
            with transaction.atomic():
                aluno = AlunoRepository.create_aluno(
                    nome=nome,
                    email=email,
                    matricula=matricula,
                    curso=curso,
                    periodo=periodo_val,
                    cr_geral=cr_val,
                    tipo_usuario=tipo_usuario,
                    data_ingresso=timezone.now().date(),
                    ativo=True
                )
            return aluno
        except IntegrityError as e:
            raise

    def update_aluno(self, aluno_id, nome=None, email=None, periodo=None, cr_geral=None, ativo=None):
        aluno = AlunoRepository.get_aluno_by_id(aluno_id)
        if nome is not None:
            aluno.nome = nome
        if email is not None:
            aluno.email = email
        if periodo is not None and periodo != '':
            try:
                aluno.periodo = int(periodo)
            except (ValueError, TypeError):
                pass
        if cr_geral is not None and cr_geral != '':
            try:
                aluno.cr_geral = float(cr_geral)
            except (ValueError, TypeError):
                pass
        if ativo is not None:
            aluno.ativo = bool(ativo)
        aluno.save()
        return aluno

    def delete_aluno(self, aluno_id):
        aluno = AlunoRepository.get_aluno_by_id(aluno_id)
        nome = aluno.nome
        aluno.delete()
        return nome
    

class TurmaService:
    """Service para operações CRUD de Turma."""

    def list_turmas(self, vaga_id=None, status=None):
        return TurmaRepository.list_turmas(vaga_id, status)

    def get_turma_detail(self, turma_id):
        turma = TurmaRepository.get_turma_by_id(turma_id)
        participacoes = TurmaRepository.get_participacoes_by_turma(turma)
        presencas = TurmaRepository.get_presencas_by_turma(turma)
        return {
            'turma': turma,
            'participacoes': participacoes,
            'presencas': presencas,
        }

    def create_turma(self, nome, vaga_id, sala_id, descricao, data_inicio, data_fim, dias_semana, horario, monitor_id, curso_id):
        try:
            with transaction.atomic():
                vaga = TurmaRepository.get_vaga_by_id(vaga_id)
                sala = TurmaRepository.get_sala_by_id(sala_id)
                monitor = TurmaRepository.get_monitor_by_id(monitor_id)
                curso = TurmaRepository.get_curso_by_id(curso_id)
                turma = TurmaRepository.create_turma(
                    nome=nome,
                    vaga=vaga,
                    sala=sala,
                    descricao=descricao,
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                    dias_da_semana=dias_semana,
                    horario=horario,
                    monitor=monitor,
                    curso=curso,
                    ativo=True
                )
            return turma
        except Exception as e:
            raise

    def update_turma(self, turma_id, nome=None, descricao=None, horario=None, ativo=None):
        turma = TurmaRepository.get_turma_by_id(turma_id)
        if nome is not None:
            turma.nome = nome
        if descricao is not None:
            turma.descricao = descricao
        if horario is not None:
            turma.horario = horario
        if ativo is not None:
            turma.ativo = ativo
        turma.save()
        return turma

    def delete_turma(self, turma_id):
        turma = TurmaRepository.get_turma_by_id(turma_id)
        turma.delete()
        return True
    

class MonitoriaService:
    """Service para operações de monitorias do professor."""

    def listar_monitorias(self, user, turma_id=None):
        try:
            professor = MonitoriaRepository.get_professor_by_email(user.email)
            turmas = MonitoriaRepository.get_turmas_by_professor(professor)
            participacoes = MonitoriaRepository.get_participacoes_by_turmas(turmas)
            if turma_id:
                participacoes = participacoes.filter(turma__id=turma_id)
                turmas = turmas.filter(id=turma_id)
        except Funcionario.DoesNotExist:
            turmas = Turma.objects.none()
            participacoes = ParticipacaoMonitoria.objects.none()
        return {
            'participacoes': participacoes,
            'turmas': turmas,
        }

    def editar_participacao(self, participacao_id, ap1=None, ap2=None, cr=None):
        participacao = MonitoriaRepository.get_participacao_by_id(participacao_id)
        participacao.ap1 = ap1 if ap1 != '' else None
        participacao.ap2 = ap2 if ap2 != '' else None
        participacao.cr = cr if cr != '' else None
        participacao.save()
        return participacao

class PresencaService:
    """Service para operações de presenças."""

    def listar_presencas(self, turma_id=None, data=None):
        presencas = PresencaRepository.list_presencas(turma_id, data)
        turmas = PresencaRepository.get_turmas_ativas()
        return {
            'presencas': presencas,
            'turmas': turmas,
        }

    def editar_presenca(self, presenca_id, presente):
        presenca = PresencaRepository.get_presenca_by_id(presenca_id)
        presenca.presente = presente
        presenca.save()

class RelatorioService:
    """Service para relatórios do sistema."""

    def desempenho(self):
        participacoes = RelatorioRepository.get_participacoes()
        return {
            'participacoes': participacoes,
            'titulo': 'Relatório de Desempenho',
        }

    def frequencia(self):
        presencas = RelatorioRepository.get_presencas()
        return {
            'presencas': presencas,
            'titulo': 'Relatório de Frequência',
        }

    def inscricoes(self):
        inscricoes = RelatorioRepository.get_inscricoes()
        return {
            'inscricoes': inscricoes,
            'titulo': 'Relatório de Inscrições',
        }

    def geral(self):
        return {
            'total_usuarios': RelatorioRepository.get_total_usuarios(),
            'total_alunos': RelatorioRepository.get_total_alunos(),
            'total_funcionarios': RelatorioRepository.get_total_funcionarios(),
            'total_turmas': RelatorioRepository.get_total_turmas(),
            'total_vagas': RelatorioRepository.get_total_vagas(),
            'total_inscricoes': RelatorioRepository.get_total_inscricoes(),
            'total_presencas': RelatorioRepository.get_total_presencas(),
            'titulo': 'Relatório Geral',
        }

class PerfilService:
    """Service para operações de perfil do usuário."""

    def get_perfil_context(self, user):
        aluno = PerfilRepository.get_aluno_by_email(user.email)
        professor = PerfilRepository.get_professor_by_email(user.email)
        return {
            'usuario': user,
            'aluno': aluno,
            'professor': professor,
        }

    def atualizar_perfil(self, user, data):
        nome = data.get('nome')
        email = data.get('email')
        user.first_name = nome
        user.email = email
        user.save()
        aluno = PerfilRepository.get_aluno_by_email(user.email)
        if aluno:
            aluno.nome = nome
            aluno.email = email
            aluno.save()




class VagaMonitoriaService:
    """Service para operações de vagas."""

    def listar_vagas(self, user, curso_filtro=None, status_filtro=None):
        if user.is_staff or user.is_superuser:
            vagas = VagaRepository.get_all_vagas()
        else:
            try:
                funcionario = Funcionario.objects.get(email=user.email)
                vagas = VagaRepository.get_vagas_by_coordenador(funcionario)
            except Funcionario.DoesNotExist:
                vagas = Vaga.objects.none()
        if curso_filtro:
            vagas = vagas.filter(curso__id=curso_filtro)
        if status_filtro:
            vagas = vagas.filter(ativo=(status_filtro == 'ativa'))
        return vagas

    def detalhe_vaga(self, vaga_id, user):
        vaga = VagaRepository.get_vaga_by_id(vaga_id)
        if not (user.is_staff or user.is_superuser):
            try:
                funcionario = Funcionario.objects.get(email=user.email)
                if funcionario not in vaga.coordenadores.all() and funcionario not in vaga.professores.all():
                    return None
            except Funcionario.DoesNotExist:
                return None
        inscricoes = VagaRepository.get_inscricoes_by_vaga(vaga)
        stats = {
            'total_inscricoes': inscricoes.count(),
            'pendentes': inscricoes.filter(status='Pendente').count(),
            'entrevista': inscricoes.filter(status='Entrevista').count(),
            'aprovados': inscricoes.filter(status='Aprovado').count(),
            'rejeitados': inscricoes.filter(status='Não Aprovado').count(),
        }
        return {'vaga': vaga, 'inscricoes': inscricoes, **stats}

    def criar_vaga(self, nome, curso_id, disciplina_id, coordenador_id, descricao, requisitos, numero_vagas, user):
        if not (user.is_staff or user.is_superuser):
            try:
                funcionario = Funcionario.objects.get(email=user.email)
                if str(funcionario.id) != str(coordenador_id):
                    return None
            except Funcionario.DoesNotExist:
                return None
        try:
            curso = VagaRepository.get_curso_by_id(curso_id)
            disciplina = VagaRepository.get_disciplina_by_id(disciplina_id)
            coordenador = VagaRepository.get_funcionario_by_id(coordenador_id)
            vaga = VagaRepository.create_vaga(
                nome=nome,
                curso=curso,
                disciplina=disciplina,
                descricao=descricao,
                requisitos=requisitos,
                numero_vagas=int(numero_vagas) if numero_vagas else 1,
                ativo=True
            )
            vaga.coordenadores.add(coordenador)
            return vaga
        except Exception:
            return None

    def editar_vaga(self, vaga_id, user, nome, descricao, requisitos, ativo, coordenadores_ids=None, professores_ids=None):
        vaga = VagaRepository.get_vaga_by_id(vaga_id)
        if not (user.is_staff or user.is_superuser):
            try:
                funcionario = Funcionario.objects.get(email=user.email)
                if funcionario not in vaga.coordenadores.all() and funcionario not in vaga.professores.all():
                    return None
            except Funcionario.DoesNotExist:
                return None
        vaga.nome = nome
        vaga.descricao = descricao
        vaga.requisitos = requisitos
        vaga.ativo = ativo
        if coordenadores_ids:
            vaga.coordenadores.set(coordenadores_ids)
        if professores_ids:
            vaga.professores.set(professores_ids)
        vaga.save()
        return vaga

    def deletar_vaga(self, vaga_id, user):
        vaga = VagaRepository.get_vaga_by_id(vaga_id)
        if not (user.is_staff or user.is_superuser):
            try:
                funcionario = Funcionario.objects.get(email=user.email)
                if funcionario not in vaga.coordenadores.all():
                    return None
            except Funcionario.DoesNotExist:
                return None
        nome = vaga.nome
        VagaRepository.delete_vaga(vaga)
        return nome
    


class TurmaService:
    """Service para operações de turmas."""

    def listar_turmas(self, vaga_filtro=None, status_filtro=None):
        turmas = TurmaRepository.get_all_turmas()
        if vaga_filtro:
            turmas = turmas.filter(vaga__id=vaga_filtro)
        if status_filtro:
            turmas = turmas.filter(ativo=(status_filtro == 'ativa'))
        return turmas

    def detalhe_turma(self, turma_id):
        turma = TurmaRepository.get_turma_by_id(turma_id)
        participacoes = TurmaRepository.get_participacoes_by_turma(turma)
        presencas = TurmaRepository.get_presencas_by_turma(turma)
        return {
            'turma': turma,
            'participacoes': participacoes,
            'presencas': presencas,
        }

    def criar_turma(self, nome, vaga_id, sala_id, descricao, data_inicio, data_fim, dias_semana, horario, monitor_id, curso_id):
        try:
            vaga = VagaRepository.get_vaga_by_id(vaga_id)
            sala = Sala.objects.get(id=sala_id)
            monitor = Aluno.objects.get(id=monitor_id)
            curso = Curso.objects.get(id=curso_id)
            turma = TurmaRepository.create_turma(
                nome=nome,
                vaga=vaga,
                sala=sala,
                descricao=descricao,
                data_inicio=data_inicio,
                data_fim=data_fim,
                dias_da_semana=dias_semana,
                horario=horario,
                monitor=monitor,
                curso=curso,
                ativo=True
            )
            return turma
        except Exception:
            return None

    def editar_turma(self, turma_id, nome, descricao, horario, ativo):
        turma = TurmaRepository.get_turma_by_id(turma_id)
        turma.nome = nome
        turma.descricao = descricao
        turma.horario = horario
        turma.ativo = ativo
        turma.save()
        return turma

    def deletar_turma(self, turma_id):
        turma = TurmaRepository.get_turma_by_id(turma_id)
        nome = turma.nome
        TurmaRepository.delete_turma(turma)
        return nome
    
class RelatorioService:
    """Service para relatórios do sistema."""

    def desempenho(self):
        participacoes = RelatorioRepository.get_participacoes()
        return {
            'participacoes': participacoes,
            'titulo': 'Relatório de Desempenho',
        }

    def frequencia(self):
        presencas = RelatorioRepository.get_presencas()
        return {
            'presencas': presencas,
            'titulo': 'Relatório de Frequência',
        }

    def inscricoes(self):
        inscricoes = RelatorioRepository.get_inscricoes()
        return {
            'inscricoes': inscricoes,
            'titulo': 'Relatório de Inscrições',
        }

    def geral(self):
        return {
            'total_usuarios': RelatorioRepository.get_total_usuarios(),
            'total_alunos': RelatorioRepository.get_total_alunos(),
            'total_funcionarios': RelatorioRepository.get_total_funcionarios(),
            'total_turmas': RelatorioRepository.get_total_turmas(),
            'total_vagas': RelatorioRepository.get_total_vagas(),
            'total_inscricoes': RelatorioRepository.get_total_inscricoes(),
            'total_presencas': RelatorioRepository.get_total_presencas(),
            'titulo': 'Relatório Geral',
        }
    

class PortalVagasService:
    def listar_vagas(self, busca=None, curso=None, tipo=None):
        vagas = PortalVagasRepository.vagas_ativas()
        vagas = PortalVagasRepository.filtrar_vagas(vagas, busca, curso, tipo)
        return vagas

    def estatisticas(self):
        return {
            'total_vagas': PortalVagasRepository.total_vagas(),
            'total_cursos': PortalVagasRepository.total_cursos(),
            'total_disciplinas': PortalVagasRepository.total_disciplinas(),
            'cursos': PortalVagasRepository.cursos_ativos(),
        }

    def get_aluno(self, email):
        return PortalVagasRepository.get_aluno_by_email(email)

    def pode_candidatar(self, aluno, vaga):
        perfil_incompleto = []
        if not aluno.curso:
            perfil_incompleto.append('Curso não cadastrado')
        if not aluno.periodo or aluno.periodo <= 0:
            perfil_incompleto.append('Período não informado')
        if not aluno.cr_geral or aluno.cr_geral <= 0:
            perfil_incompleto.append('CR (Coeficiente de Rendimento) não informado')
        if not aluno.celular:
            perfil_incompleto.append('Celular não informado')
        return perfil_incompleto

    def candidatar(self, aluno, vaga, arquivos):
        if PortalVagasRepository.inscricao_exists(aluno, vaga):
            return None, 'Já inscrito'
        if PortalVagasRepository.vagas_disponiveis(vaga) <= 0:
            return None, 'Sem vagas disponíveis'
        inscricao = PortalVagasRepository.criar_inscricao(aluno, vaga)
        # Histórico Escolar obrigatório
        historico = arquivos.get('documento_histórico_escolar')
        if not historico:
            return None, 'Histórico Escolar obrigatório'
        PortalVagasRepository.criar_documento(inscricao, 'Histórico Escolar', historico, historico.name)
        # Opcionais
        for field, tipo_doc in {'documento_currículo': 'Currículo', 'documento_carta_de_motivação': 'Carta de Motivação'}.items():
            arquivo = arquivos.get(field)
            if arquivo:
                PortalVagasRepository.criar_documento(inscricao, tipo_doc, arquivo, arquivo.name)
        return inscricao, None
    

class RegistroHorasService:
    def get_turmas_do_monitor(self, monitor):
        return RegistroHorasRepository.get_turmas_do_monitor(monitor)

    def criar_registro(self, turma_id, monitor, data, hora_inicio, hora_fim, descricao_atividade):
        turma = Turma.objects.get(id=turma_id, monitor=monitor, ativo=True)
        return RegistroHorasRepository.criar_registro(turma, monitor, data, hora_inicio, hora_fim, descricao_atividade)

    def get_registros_do_monitor(self, monitor):
        return RegistroHorasRepository.get_registros_do_monitor(monitor)

    def get_registro_by_id_monitor(self, registro_id, monitor):
        return RegistroHorasRepository.get_registro_by_id_monitor(registro_id, monitor)

    def get_funcionario_by_email(self, email):
        return RegistroHorasRepository.get_funcionario_by_email(email)

    def get_registros_pendentes(self):
        return RegistroHorasRepository.get_registros_pendentes()

    def get_registro_by_id(self, registro_id):
        return RegistroHorasRepository.get_registro_by_id(registro_id)
    
    def get_monitor_by_email(self, email):
        return RegistroHorasRepository.get_monitor_by_email(email)


    def aprovar_registro(self, registro, funcionario, status, observacao):
        registro.status = status
        registro.observacao_validador = observacao
        registro.validado_por = funcionario
        registro.data_validacao = timezone.now()
        registro.save()
        return registro
    

class DashboardGestaoService:
    def get_dashboard_context(self):
        seis_meses_atras = timezone.now() - timedelta(days=180)
        inscricoes_timeline = DashboardGestaoRepository.inscricoes_timeline(seis_meses_atras)
        horas_timeline = DashboardGestaoRepository.horas_timeline(seis_meses_atras)
        pagamentos_timeline = DashboardGestaoRepository.pagamentos_timeline(seis_meses_atras)

        # Preparar labels e valores para gráficos
        timeline_labels = [item['mes'].strftime('%Y-%m') if item['mes'] else '' for item in inscricoes_timeline]
        timeline_values = [item['total'] for item in inscricoes_timeline]
        horas_labels = [item['mes'].strftime('%Y-%m') if item['mes'] else '' for item in horas_timeline]
        horas_values = [float(item['total_horas']) for item in horas_timeline]
        pagamentos_dict = {item['mes'].strftime('%Y-%m') if item['mes'] else '': float(item['total_valor']) for item in pagamentos_timeline}
        valores_pagamento = [pagamentos_dict.get(mes, 0) for mes in horas_labels]

        inscricoes_por_status = DashboardGestaoRepository.inscricoes_por_status()
        status_labels = [item['status'] for item in inscricoes_por_status]
        status_values = [item['total'] for item in inscricoes_por_status]

        monitores_por_curso = DashboardGestaoRepository.monitores_por_curso()
        curso_labels = [item['aluno__curso__nome'] for item in monitores_por_curso]
        curso_values = [item['total'] for item in monitores_por_curso]

        horas_por_status = DashboardGestaoRepository.horas_por_status()
        horas_status_labels = [item['status'] for item in horas_por_status]
        horas_status_values = [item['total'] for item in horas_por_status]

        total_pago_ano = DashboardGestaoRepository.total_pago_ano()
        media_mensal = total_pago_ano / timezone.now().month if timezone.now().month > 0 else 0

        context = {
            'total_monitores': DashboardGestaoRepository.total_monitores(),
            'total_alunos': DashboardGestaoRepository.total_alunos(),
            'total_professores': DashboardGestaoRepository.total_professores(),
            'total_vagas': DashboardGestaoRepository.total_vagas(),
            'total_turmas': DashboardGestaoRepository.total_turmas(),
            'total_inscricoes': DashboardGestaoRepository.total_inscricoes(),
            'total_horas_mes': round(DashboardGestaoRepository.total_horas_mes(), 2),
            'valor_total_mes': round(DashboardGestaoRepository.valor_total_mes(), 2),
            'inscricoes_por_status': inscricoes_por_status,
            'status_labels': json.dumps(status_labels),
            'status_values': json.dumps(status_values),
            'taxa_aprovacao': DashboardGestaoRepository.taxa_aprovacao(),
            'monitores_por_curso': monitores_por_curso,
            'curso_labels': json.dumps(curso_labels),
            'curso_values': json.dumps(curso_values),
            'timeline_labels': json.dumps(timeline_labels),
            'timeline_values': json.dumps(timeline_values),
            'horas_labels': json.dumps(horas_labels),
            'horas_values': json.dumps(horas_values),
            'valores_pagamento': json.dumps(valores_pagamento),
            'horas_status_labels': json.dumps(horas_status_labels),
            'horas_status_values': json.dumps(horas_status_values),
            'pagamentos_pendentes': DashboardGestaoRepository.pagamentos_pendentes(),
            'avaliacoes_pendentes': DashboardGestaoRepository.avaliacoes_pendentes(),
            'horas_pendentes': DashboardGestaoRepository.horas_pendentes(),
            'documentos_pendentes': DashboardGestaoRepository.documentos_pendentes(),
            'vagas_ativas': DashboardGestaoRepository.vagas_ativas(),
            'cr_medio_monitores': round(DashboardGestaoRepository.cr_medio_monitores(), 2),
            'media_horas_monitor': round(DashboardGestaoRepository.media_horas_monitor(), 2),
            'total_pago_ano': round(total_pago_ano, 2),
            'media_mensal': round(media_mensal, 2),
            'now': timezone.now(),
        }
        return context
    

class DisciplinaService:
    def listar_disciplinas(self, curso=None, periodo=None, busca=None):
        return DisciplinaRepository.listar_disciplinas(
            ativo=True,
            curso_id=curso,
            periodo=periodo,
            busca=busca
        )

    def get_cursos_ativos(self):
        return DisciplinaRepository.get_cursos_ativos()

    def get_disciplina(self, disciplina_id):
        return DisciplinaRepository.get_disciplina_by_id(disciplina_id)

    def pode_editar(self, disciplina, user):
        if user.is_staff or user.is_superuser:
            return True
        funcionario = DisciplinaRepository.get_funcionario_by_email(user.email)
        return funcionario and disciplina.criado_por == funcionario
    


class RegistroService:
    def validar_dados(self, nome, email, matricula, curso_id, password, password_confirm, terms):
        erros = []
        if not all([nome, email, matricula, curso_id, password]):
            erros.append('Por favor, preencha todos os campos obrigatórios.')
        if not terms:
            erros.append('Você deve aceitar os Termos de Serviço e Política de Privacidade.')
        if password != password_confirm:
            erros.append('As senhas não correspondem!')
        if len(password) < 8:
            erros.append('A senha deve ter no mínimo 8 caracteres.')
        if not any(c.isupper() for c in password):
            erros.append('A senha deve conter pelo menos 1 letra maiúscula.')
        if not any(c.islower() for c in password):
            erros.append('A senha deve conter pelo menos 1 letra minúscula.')
        if not any(c.isdigit() for c in password):
            erros.append('A senha deve conter pelo menos 1 número.')
        if RegistroRepository.email_existe(email):
            erros.append('Este email já está cadastrado.')
        if RegistroRepository.matricula_existe(matricula):
            erros.append('Esta matrícula já está cadastrada.')
        try:
            RegistroRepository.get_curso(curso_id)
        except:
            erros.append('Curso inválido.')
        return erros

    def gerar_username_unico(self, email):
        username = email.split('@')[0] if email else ''
        base_username = username
        counter = 1
        while RegistroRepository.username_existe(username):
            username = f"{base_username}{counter}"
            counter += 1
        return username

    def registrar_usuario_aluno(self, nome, email, matricula, curso_id, password):
        username = self.gerar_username_unico(email)
        user = RegistroRepository.criar_usuario(username, email, password, nome)
        grupo_aluno = RegistroRepository.get_grupo_aluno()
        RegistroRepository.adicionar_grupo(user, grupo_aluno)
        tipo_usuario = RegistroRepository.get_tipo_usuario_aluno()
        curso = RegistroRepository.get_curso(curso_id)
        periodo = 1
        cr_geral = 0.0
        aluno = RegistroRepository.criar_aluno(
            nome, email, tipo_usuario, matricula, curso, periodo, cr_geral
        )
        return user, aluno
    

class AuthService:
    def autenticar_usuario(self, request, username, password):
        return AuthRepository.autenticar(request, username, password)

    def logout(self, request):
        AuthRepository.logout_usuario(request)