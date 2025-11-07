"""
Middleware personalizado para melhorar compatibilidade mobile
"""
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class MobileCompatibilityMiddleware(MiddlewareMixin):
    """
    Middleware para melhorar compatibilidade com dispositivos móveis
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_request(self, request):
        """
        Processa request e adiciona informações sobre mobile
        """
        # Detectar se é mobile
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        mobile_keywords = [
            'mobile', 'android', 'iphone', 'ipad', 'ipod', 
            'blackberry', 'windows phone', 'opera mini'
        ]
        
        request.is_mobile = any(keyword in user_agent for keyword in mobile_keywords)
        
        # Log para debug
        if request.is_mobile:
            logger.info(f"Mobile request detected: {user_agent}")
        
        return None
    
    def process_exception(self, request, exception):
        """
        Processa exceções e fornece respostas específicas para mobile
        """
        logger.error(f"Exception in mobile middleware: {exception}")
        
        # Se for mobile e uma exceção crítica, retornar página de erro simples
        if getattr(request, 'is_mobile', False):
            try:
                # Para requests AJAX, retornar JSON
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'error': True,
                        'message': 'Erro interno do servidor. Tente novamente.',
                        'mobile_friendly': True
                    }, status=500)
                
                # Para requests normais, página de erro simples
                context = {
                    'error_message': 'Ops! Algo deu errado.',
                    'error_details': 'Tente recarregar a página ou verifique sua conexão.',
                    'is_mobile': True
                }
                
                return render(request, 'errors/mobile_error.html', context, status=500)
                
            except Exception as e:
                logger.error(f"Error in mobile error handling: {e}")
                # Fallback para resposta mínima
                return JsonResponse({
                    'error': True,
                    'message': 'Erro do servidor'
                }, status=500)
        
        return None


class MobileOptimizationMiddleware(MiddlewareMixin):
    """
    Middleware para otimizações específicas de mobile
    """
    
    def process_response(self, request, response):
        """
        Otimiza response para mobile
        """
        if getattr(request, 'is_mobile', False):
            # Adicionar headers específicos para mobile
            response['X-Mobile-Optimized'] = 'true'
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            
            # Headers para PWA
            response['X-Content-Type-Options'] = 'nosniff'
            response['X-Frame-Options'] = 'SAMEORIGIN'
        
        return response