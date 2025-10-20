from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Remove is_staff flag from professor.teste user'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username='professor.teste')
            if user.is_staff:
                self.stdout.write(f'Antes: is_staff={user.is_staff}')
                user.is_staff = False
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Removido is_staff de professor.teste'))
                self.stdout.write(f'Depois: is_staff={user.is_staff}')
            else:
                self.stdout.write('professor.teste já tem is_staff=False')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('professor.teste não encontrado'))
