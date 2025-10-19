"""
Management Command: sincronizar_grupos.py

Sincroniza automaticamente os grupos de Django Users com base nas vagas coordenadas

Uso:
    python manage.py sincronizar_grupos

Descrição:
    ✅ Adiciona grupo "Coordenador" para Professores que coordenam vagas
    ✅ Remove grupo "Coordenador" para Professores que não coordenam mais vagas
    ✅ Cria grupo "Coordenador" se não existir
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from plataforma_Casa.models import Funcionario, Vaga


class Command(BaseCommand):
    help = 'Sincroniza grupos de usuários: Adiciona "Coordenador" para professores com vagas'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔄 Iniciando sincronização de grupos...\n'))
        
        # ========== CRIAR GRUPO "COORDENADOR" SE NÃO EXISTIR ==========
        grupo_coordenador, created = Group.objects.get_or_create(name='Coordenador')
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Grupo "Coordenador" criado com sucesso'))
        else:
            self.stdout.write('ℹ️  Grupo "Coordenador" já existe')
        
        self.stdout.write('\n' + '='*60)
        
        # ========== SINCRONIZAR PROFESSORES ==========
        self.stdout.write(self.style.WARNING('📋 PROCESSANDO PROFESSORES\n'))
        
        grupo_professor, _ = Group.objects.get_or_create(name='Professor')
        professores = User.objects.filter(groups__name='Professor')
        
        total_professores = professores.count()
        adicionados = 0
        removidos = 0
        
        self.stdout.write(f'Total de Professores: {total_professores}\n')
        
        for user in professores:
            try:
                # Buscar Funcionario correspondente
                funcionario = Funcionario.objects.get(email=user.email)
                
                # Contar vagas que ele coordena
                vagas_coordenadas = Vaga.objects.filter(coordenador=funcionario).count()
                
                tem_grupo_coordenador = user.groups.filter(name='Coordenador').exists()
                
                # ✅ CASO 1: Tem vagas E não tem o grupo → ADICIONAR
                if vagas_coordenadas > 0 and not tem_grupo_coordenador:
                    user.groups.add(grupo_coordenador)
                    adicionados += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'  ✅ ADICIONADO: {funcionario.nome} ({vagas_coordenadas} vagas)'
                    ))
                
                # ✅ CASO 2: Não tem vagas E tem o grupo → REMOVER
                elif vagas_coordenadas == 0 and tem_grupo_coordenador:
                    user.groups.remove(grupo_coordenador)
                    removidos += 1
                    self.stdout.write(self.style.WARNING(
                        f'  ❌ REMOVIDO: {funcionario.nome} (nenhuma vaga coordenada)'
                    ))
                
                # ✅ CASO 3: Tem vagas E tem o grupo → JÁ OK
                elif vagas_coordenadas > 0 and tem_grupo_coordenador:
                    self.stdout.write(f'  ✅ OK: {funcionario.nome} ({vagas_coordenadas} vagas)')
                
                # ✅ CASO 4: Sem vagas E sem grupo → JÁ OK
                else:
                    self.stdout.write(f'  ℹ️  SEM VAGAS: {funcionario.nome}')
                    
            except Funcionario.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f'  ❌ ERRO: Não encontrado Funcionario para {user.email}'
                ))
        
        self.stdout.write('\n' + '='*60 + '\n')
        
        # ========== RESUMO ==========
        self.stdout.write(self.style.SUCCESS('📊 RESUMO DA SINCRONIZAÇÃO:\n'))
        self.stdout.write(f'  ✅ Adicionados: {adicionados}')
        self.stdout.write(f'  ❌ Removidos: {removidos}')
        self.stdout.write(f'  📋 Total processado: {total_professores}')
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('\n✨ Sincronização concluída com sucesso!\n'))
