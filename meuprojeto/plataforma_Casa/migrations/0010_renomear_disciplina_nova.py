# Generated manually to fix disciplina field

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma_Casa', '0009_alter_disciplina_options_and_more'),
    ]

    operations = [
        # Passo 1: Remover o campo disciplina antigo (VARCHAR)
        migrations.RemoveField(
            model_name='vaga',
            name='disciplina',
        ),
        
        # Passo 2: Renomear disciplina_nova para disciplina
        migrations.RenameField(
            model_name='vaga',
            old_name='disciplina_nova',
            new_name='disciplina',
        ),
    ]
