# Generated by Django 4.2.5 on 2023-09-19 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0005_alter_emi_emi_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emi',
            name='emi_date',
            field=models.DateField(unique=True),
        ),
    ]