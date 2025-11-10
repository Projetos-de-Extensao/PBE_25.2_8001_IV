from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .permission import (
            is_adm, 
            is_admin_user, 
            is_aluno_access, 
            is_monitor_access, 
            is_funcionairo_access
            )

from .models import Vaga, Inscricao, Curso, Al


# Criado o VagaService para encapsular a lógica de negócio da view detalhe_vaga
@login_required
@user_passes_test(is_funcionairo_access)
def detalhe_vaga(request, vaga_id):
    """
    View refatorada: delega toda lógica para VagaService e apenas renderiza o contexto.
    """
    try:
        service = VagaService(vaga_id, request.user)
        context = service.get_context()
    except PermissionDenied:
        messages.error(request, '❌ Você não tem permissão para ver esta vaga')
        return redirect('listar_vagas')
    except Exception as e:
        messages.error(request, f'❌ Erro ao carregar vaga: {str(e)}')
        return redirect('listar_vagas')

    return render(request, 'vagas/detalhe.html', context)

