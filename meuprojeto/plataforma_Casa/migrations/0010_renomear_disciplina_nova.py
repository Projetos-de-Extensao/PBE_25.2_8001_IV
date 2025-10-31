# Generated manually to fix disciplina field
# Usa SQL crua para evitar problemas com cache do Django

from django.db import migrations


def renomear_disciplina_nova(apps, schema_editor):
    """
    Remove o campo disciplina antigo (VARCHAR) e
    renomeia disciplina_nova_id para disciplina_id
    """
    with schema_editor.connection.cursor() as cursor:
        # Passo 1: Remover o campo disciplina antigo (VARCHAR) se existir
        cursor.execute("""
            DO $$ 
            BEGIN
                IF EXISTS (
                    SELECT 1 
                    FROM information_schema.columns 
                    WHERE table_name = 'plataforma_Casa_vaga' 
                    AND column_name = 'disciplina'
                    AND data_type = 'character varying'
                ) THEN
                    ALTER TABLE plataforma_Casa_vaga DROP COLUMN disciplina;
                END IF;
            END $$;
        """)
        
        # Passo 2: Renomear disciplina_nova_id para disciplina_id se necessário
        cursor.execute("""
            DO $$ 
            BEGIN
                IF EXISTS (
                    SELECT 1 
                    FROM information_schema.columns 
                    WHERE table_name = 'plataforma_Casa_vaga' 
                    AND column_name = 'disciplina_nova_id'
                ) THEN
                    ALTER TABLE plataforma_Casa_vaga 
                    RENAME COLUMN disciplina_nova_id TO disciplina_id;
                END IF;
            END $$;
        """)


def reverter_renomeacao(apps, schema_editor):
    """
    Reverte as mudanças (para rollback)
    """
    with schema_editor.connection.cursor() as cursor:
        # Reverter renomeação
        cursor.execute("""
            DO $$ 
            BEGIN
                IF EXISTS (
                    SELECT 1 
                    FROM information_schema.columns 
                    WHERE table_name = 'plataforma_Casa_vaga' 
                    AND column_name = 'disciplina_id'
                ) THEN
                    ALTER TABLE plataforma_Casa_vaga 
                    RENAME COLUMN disciplina_id TO disciplina_nova_id;
                END IF;
            END $$;
        """)


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma_Casa', '0009_alter_disciplina_options_and_more'),
    ]

    operations = [
        migrations.RunPython(renomear_disciplina_nova, reverter_renomeacao),
    ]
