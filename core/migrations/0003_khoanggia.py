# Generated by Django 3.2 on 2021-05-09 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210509_0814'),
    ]

    operations = [
        migrations.CreateModel(
            name='KhoangGia',
            fields=[
                ('MaKG', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('Gia_Min', models.BigIntegerField()),
                ('Gia_Max', models.BigIntegerField()),
            ],
            options={
                'db_table': 'KHOANGGIA',
            },
        ),
    ]
