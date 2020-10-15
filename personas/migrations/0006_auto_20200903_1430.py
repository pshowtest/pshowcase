# Generated by Django 3.1 on 2020-09-03 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0005_categoria_icono_categoria'),
    ]

    operations = [
        migrations.RenameField(
            model_name='colaboracion',
            old_name='id_proyecto',
            new_name='proyecto',
        ),
        migrations.RenameField(
            model_name='colaboracion',
            old_name='id_tipo_permiso',
            new_name='tipo_permiso',
        ),
        migrations.RenameField(
            model_name='colaboracion',
            old_name='id_usuario',
            new_name='usuario',
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200)),
                ('alma_mater', models.CharField(max_length=200)),
                ('carrera', models.CharField(max_length=200)),
                ('retrato', models.CharField(max_length=200)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personas.usuario')),
            ],
        ),
    ]
