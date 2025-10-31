# Generated manually

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma_Casa', '0006_materialapoio'),
    ]

    operations = [
        # Primeiro, criar o modelo Disciplina
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(help_text='Código da disciplina (ex: CC1001)', max_length=20, unique=True)),
                ('nome', models.CharField(help_text='Nome completo da disciplina', max_length=200)),
                ('carga_horaria', models.IntegerField(default=60, help_text='Carga horária total em horas')),
                ('periodo_sugerido', models.IntegerField(blank=True, help_text='Período sugerido no curso', null=True)),
                ('ementa', models.TextField(blank=True, help_text='Ementa da disciplina', null=True)),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('curso', models.ForeignKey(help_text='Curso ao qual a disciplina pertence', on_delete=django.db.models.deletion.CASCADE, related_name='disciplinas', to='plataforma_Casa.curso')),
                ('criado_por', models.ForeignKey(blank=True, help_text='Professor que criou a disciplina', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='disciplinas_criadas', to='plataforma_Casa.funcionario')),
                ('pre_requisitos', models.ManyToManyField(blank=True, help_text='Disciplinas pré-requisitos', related_name='disciplinas_dependentes', to='plataforma_Casa.disciplina')),
            ],
            options={
                'verbose_name': 'Disciplina',
                'verbose_name_plural': 'Disciplinas',
                'ordering': ['curso', 'codigo'],
            },
        ),
        
        # Adicionar campo temporário para disciplina em Vaga (permitir null)
        migrations.AddField(
            model_name='vaga',
            name='disciplina_nova',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vagas', to='plataforma_Casa.disciplina', help_text="Disciplina da vaga"),
        ),
        
        # Adicionar novos campos em Vaga
        migrations.AddField(
            model_name='vaga',
            name='tipo_vaga',
            field=models.CharField(
                choices=[('TEA', 'TEA - Monitoria Remunerada'), ('Voluntaria', 'Monitoria Voluntária')],
                default='Voluntaria',
                help_text='Tipo de monitoria: TEA (remunerada) ou Voluntária',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='vaga',
            name='valor_bolsa',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Valor da bolsa para monitoria TEA (R$ 1.500,00 por semestre)',
                max_digits=10,
                null=True
            ),
        ),
        
        # Remover o campo antigo coordenador (ForeignKey)
        migrations.RemoveField(
            model_name='vaga',
            name='coordenador',
        ),
        
        # Adicionar o novo campo coordenadores (ManyToMany)
        migrations.AddField(
            model_name='vaga',
            name='coordenadores',
            field=models.ManyToManyField(
                help_text='Coordenadores responsáveis pela vaga',
                limit_choices_to={'coordenador': True},
                related_name='vagas_como_coordenador',
                to='plataforma_Casa.funcionario'
            ),
        ),
        
        # Adicionar o campo professores (ManyToMany)
        migrations.AddField(
            model_name='vaga',
            name='professores',
            field=models.ManyToManyField(
                blank=True,
                help_text='Professores associados à vaga',
                limit_choices_to={'funcao': 'Professor'},
                related_name='vagas_como_professor',
                to='plataforma_Casa.funcionario'
            ),
        ),
    ]
