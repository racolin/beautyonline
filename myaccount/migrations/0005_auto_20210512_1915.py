# Generated by Django 3.2 on 2021-05-12 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myaccount', '0004_auto_20210512_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hoadon',
            name='DiaChiNhan',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='hoadon',
            name='SDTNgNhan',
            field=models.CharField(max_length=11),
        ),
    ]