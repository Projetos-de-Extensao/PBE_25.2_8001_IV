"""
Backend de autenticação customizado para permitir login com email ou username
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Backend de autenticação que permite login com email ou username
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        
        if username is None or password is None:
            return None
        
        # Tentar encontrar usuário por username
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            # Se não encontrar por username, tentar por email
            try:
                user = UserModel.objects.get(email=username)
            except UserModel.DoesNotExist:
                # Executar hasher padrão para prevenir timing attacks
                UserModel().set_password(password)
                return None
        
        # Verificar senha
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
