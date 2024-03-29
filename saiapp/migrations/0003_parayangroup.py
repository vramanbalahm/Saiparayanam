# Generated by Django 2.2 on 2022-01-06 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('saiapp', '0002_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParayanGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GrpID', models.IntegerField(verbose_name='ID')),
                ('GrpName', models.CharField(max_length=100, verbose_name='Name')),
                ('GrpTeacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saiapp.Teacher')),
            ],
        ),
    ]
