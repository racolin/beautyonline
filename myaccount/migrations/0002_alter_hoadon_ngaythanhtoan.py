# Generated by Django 3.2 on 2021-05-12 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myaccount', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hoadon',
            name='NgayThanhToan',
            field=models.DateTimeField(),
        ),
    ]
