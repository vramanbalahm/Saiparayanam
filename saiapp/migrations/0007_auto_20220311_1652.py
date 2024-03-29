# Generated by Django 2.2 on 2022-03-11 11:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saiapp', '0006_auto_20220311_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devotee',
            name='RollNumber',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(48)], verbose_name='Roll No.'),
        ),
        migrations.AlterUniqueTogether(
            name='devotee',
            unique_together={('GrpID', 'RollNumber')},
        ),
    ]
