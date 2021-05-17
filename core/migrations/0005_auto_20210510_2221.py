# Generated by Django 3.2 on 2021-05-10 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_delete_khoanggia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='khachhang',
            name='UserName',
        ),
        migrations.AlterField(
            model_name='khachhang',
            name='MaXa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.xa'),
        ),
        migrations.AlterField(
            model_name='khachhang',
            name='SDT',
            field=models.CharField(max_length=11, null=True),
        ),
    ]