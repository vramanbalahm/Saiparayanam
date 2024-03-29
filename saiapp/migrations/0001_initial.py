# Generated by Django 2.0 on 2021-12-25 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Testchapters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rollnumber', models.IntegerField()),
                ('currentchapters', models.CharField(db_column='CurrentChapters', max_length=50)),
                ('parayandate', models.DateField(db_column='Parayandate')),
                ('house', models.CharField(db_column='House', max_length=10)),
                ('genstatus', models.IntegerField(db_column='Genstatus')),
                ('gendate', models.DateTimeField(db_column='Gendate')),
            ],
            options={
                'db_table': 'testchapters',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Weekchapters',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rollnumber', models.IntegerField()),
                ('currentchapters', models.CharField(db_column='CurrentChapters', max_length=50)),
                ('parayandate', models.DateField(db_column='Parayandate')),
                ('house', models.CharField(db_column='House', max_length=10)),
                ('genstatus', models.IntegerField(db_column='Genstatus')),
                ('gendate', models.DateTimeField(db_column='Gendate')),
            ],
            options={
                'db_table': 'weekchapters',
            },
        ),
    ]
