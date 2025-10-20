# Generated manually for deployment
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma_Casa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaga',
            name='responsabilidades',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vaga',
            name='numero_vagas',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='vaga',
            name='disciplina',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
