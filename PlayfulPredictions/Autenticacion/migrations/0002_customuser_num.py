# Generated by Django 5.0.2 on 2024-04-24 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Autenticacion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='num',
            field=models.IntegerField(default=0),
        ),
    ]