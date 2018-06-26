# Generated by Django 2.0.6 on 2018-06-26 22:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_cate', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.CharField(max_length=70)),
                ('fecha_comentario', models.DateField()),
                ('fimg', models.ImageField(blank=True, default='', null=True, upload_to='imgs')),
            ],
        ),
        migrations.CreateModel(
            name='Objeto_Aprendizaje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('descripcion', models.CharField(max_length=50)),
                ('fecha_creacion', models.DateField()),
                ('fzip', models.FileField(blank=True, default='vacio.zip', null=True, upload_to='storage')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='objetos_aprendizaje.Categoria')),
            ],
        ),
    ]
