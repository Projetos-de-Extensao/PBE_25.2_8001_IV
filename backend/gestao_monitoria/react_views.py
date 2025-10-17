from django.views.generic import TemplateView
from django.conf import settings
import logging
import os

logger = logging.getLogger(__name__)


class ReactAppView(TemplateView):
    """
    View para servir a aplicação React compilada.
    Esta view serve o index.html do build do React e permite que o React Router
    funcione corretamente em todas as rotas do frontend.
    """
    template_name = 'index.html'

    def get_template_names(self):
        """
        Verifica se o build do React existe antes de servir.
        Se não existir, retorna um template de instruções.
        """
        react_build_path = settings.REACT_APP_DIR / 'build' / 'index.html'
        
        if react_build_path.exists():
            return ['index.html']
        else:
            logger.error(
                f"React build não encontrado em {react_build_path}. "
                f"Execute 'npm run build' no diretório frontend."
            )
            return ['react_build_missing.html']

    def get_context_data(self, **kwargs):
        """Adiciona informações sobre o build do React ao contexto."""
        context = super().get_context_data(**kwargs)
        react_build_path = settings.REACT_APP_DIR / 'build' / 'index.html'
        context['react_build_exists'] = react_build_path.exists()
        return context
