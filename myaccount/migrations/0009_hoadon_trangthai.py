# Generated by Django 3.2.13 on 2022-05-25 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myaccount', '0008_remove_hoadon_diachigh'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoadon',
            name='TrangThai',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
