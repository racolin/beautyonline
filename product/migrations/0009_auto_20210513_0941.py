# Generated by Django 3.2 on 2021-05-13 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_sapxep_masx'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='Rate',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='ThoiGian',
            field=models.DateTimeField(null=True),
        ),
    ]