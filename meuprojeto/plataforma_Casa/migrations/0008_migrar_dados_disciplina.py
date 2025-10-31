# Generated manually

from django.db import migrations, models
import django.db.models.deletion


def criar_disciplinas_das_vagas(apps, schema_editor):
    """
    Cria disciplinas a partir dos nomes existentes nas vagas
    e associa as vagas às disciplinas criadas
    """
    Vaga = apps.get_model('plataforma_Casa', 'Vaga')
    Disciplina = apps.get_model('plataforma_Casa', 'Disciplina')
    
    # Mapeia nomes de disciplinas para objetos Disciplina
    disciplinas_map = {}
    
    for vaga in Vaga.objects.all():
        if hasattr(vaga, 'disciplina') and vaga.disciplina:
            # Se disciplina era um CharField com nome
            nome_disciplina = str(vaga.disciplina).strip()
            
            if nome_disciplina not in disciplinas_map:
                # Criar nova disciplina
                disciplina = Disciplina.objects.create(
                    codigo=f'DISC{len(disciplinas_map) + 1:03d}',
                    nome=nome_disciplina,
                    curso=vaga.curso,
                    carga_horaria=60,
                    ativo=True
                )
                disciplinas_map[nome_disciplina] = disciplina
            
            # Associar vaga à disciplina
            vaga.disciplina_nova = disciplinas_map[nome_disciplina]
            vaga.save()


def reverter_disciplinas(apps, schema_editor):
    """Função de reversão (não faz nada pois não podemos reverter facilmente)"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma_Casa', '0007_criar_disciplina_e_atualizar_vaga'),
    ]

    operations = [
        migrations.RunPython(criar_disciplinas_das_vagas, reverter_disciplinas),
        
        # Remover o campo antigo disciplina (CharField)
        migrations.RemoveField(
            model_name='vaga',
            name='disciplina',
        ),
        
        # Renomear disciplina_nova para disciplina
        migrations.RenameField(
            model_name='vaga',
            old_name='disciplina_nova',
            new_name='disciplina',
        ),
        
        # Alterar o campo para não permitir null
        migrations.AlterField(
            model_name='vaga',
            name='disciplina',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='vagas',
                to='plataforma_Casa.disciplina',
                help_text="Disciplina da vaga"
            ),
        ),
    ]
