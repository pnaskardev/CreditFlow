# Generated by Django 4.2.5 on 2023-09-19 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0006_alter_emi_emi_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emi',
            name='emi_date',
            field=models.DateField(),
        ),
    ]
