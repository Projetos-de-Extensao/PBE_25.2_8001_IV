# Generated manually for deployment
from django.db import migrations, models
import django.db.models.deletion
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma_Casa', '0002_adicionar_campos_vaga'),
    ]

    operations = [
        # Criar modelo Documento
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(
                    max_length=50,
                    choices=[
                        ('Histórico Escolar', 'Histórico Escolar'),
                        ('Currículo', 'Currículo'),
                        ('Carta de Motivação', 'Carta de Motivação'),
                        ('Outro', 'Outro'),
                    ]
                )),
                ('arquivo', models.FileField(upload_to='documentos/%Y/%m/%d/')),
                ('nome_arquivo', models.CharField(max_length=255)),
                ('enviado_em', models.DateTimeField(auto_now_add=True)),
                ('observacao', models.TextField(blank=True, null=True)),
                ('inscricao', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='documentos',
                    to='plataforma_Casa.inscricao'
                )),
            ],
        ),
        
        # Criar modelo RegistroHoras
        migrations.CreateModel(
            name='RegistroHoras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fim', models.TimeField()),
                ('total_horas', models.DecimalField(max_digits=5, decimal_places=2, editable=False)),
                ('descricao_atividade', models.TextField()),
                ('status', models.CharField(
                    max_length=50,
                    choices=[
                        ('Pendente', 'Pendente'),
                        ('Aprovado', 'Aprovado'),
                        ('Rejeitado', 'Rejeitado'),
                    ],
                    default='Pendente'
                )),
                ('data_validacao', models.DateTimeField(null=True, blank=True)),
                ('observacao_validador', models.TextField(blank=True, null=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('turma', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='registros_horas',
                    to='plataforma_Casa.turma'
                )),
                ('monitor', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='horas_registradas',
                    to='plataforma_Casa.aluno'
                )),
                ('validado_por', models.ForeignKey(
                    on_delete=django.db.models.deletion.SET_NULL,
                    null=True,
                    blank=True,
                    related_name='horas_validadas',
                    to='plataforma_Casa.funcionario'
                )),
            ],
            options={
                'verbose_name': 'Registro de Horas',
                'verbose_name_plural': 'Registros de Horas',
                'ordering': ['-data', '-hora_inicio'],
            },
        ),
        
        # Criar modelo StatusPagamento
        migrations.CreateModel(
            name='StatusPagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes_referencia', models.DateField(help_text="Data final do semestre para este pagamento")),
                ('valor_total', models.DecimalField(
                    max_digits=10,
                    decimal_places=2,
                    editable=False,
                    default=Decimal('1500.00')
                )),
                ('status', models.CharField(
                    max_length=50,
                    choices=[
                        ('Pendente', 'Pendente'),
                        ('Processando', 'Processando'),
                        ('Pago', 'Pago'),
                        ('Cancelado', 'Cancelado'),
                    ],
                    default='Pendente'
                )),
                ('data_processamento', models.DateTimeField(null=True, blank=True)),
                ('observacao', models.TextField(
                    blank=True,
                    null=True,
                    help_text="Observações sobre o pagamento"
                )),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('monitor', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='pagamentos',
                    to='plataforma_Casa.aluno'
                )),
                ('turma', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='pagamentos',
                    to='plataforma_Casa.turma'
                )),
                ('processado_por', models.ForeignKey(
                    on_delete=django.db.models.deletion.SET_NULL,
                    null=True,
                    blank=True,
                    related_name='pagamentos_processados',
                    to='plataforma_Casa.funcionario'
                )),
            ],
            options={
                'verbose_name': 'Status de Pagamento',
                'verbose_name_plural': 'Status de Pagamentos',
                'ordering': ['-mes_referencia'],
            },
        ),
    ]
