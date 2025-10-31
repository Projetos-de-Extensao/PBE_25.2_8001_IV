# Generated manually to fix disciplina field

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma_Casa', '0009_alter_disciplina_options_and_more'),
    ]

    operations = [
        # Renomear disciplina_nova para disciplina
        migrations.RenameField(
            model_name='vaga',
            old_name='disciplina_nova',
            new_name='disciplina',
        ),
    ]
