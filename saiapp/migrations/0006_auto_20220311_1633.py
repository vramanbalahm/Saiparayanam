# Generated by Django 2.2 on 2022-03-11 11:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saiapp', '0005_auto_20220215_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devotee',
            name='RollNumber',
            field=models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(48)], verbose_name='Roll No.'),
        ),
    ]
