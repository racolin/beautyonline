# Generated by Django 3.2.13 on 2022-05-25 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_lienhe_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='khachhang',
            name='SignDate',
            field=models.DateTimeField(null=True),
        ),
    ]
