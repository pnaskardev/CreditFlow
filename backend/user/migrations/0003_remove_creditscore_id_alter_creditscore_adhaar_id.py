# Generated by Django 4.2.5 on 2023-09-17 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_creditscore'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditscore',
            name='id',
        ),
        migrations.AlterField(
            model_name='creditscore',
            name='adhaar_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='credit_score', serialize=False, to='user.customer'),
        ),
    ]
