# Generated by Django 4.2.5 on 2023-09-17 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_score', models.IntegerField(default=0)),
                ('adhaar_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='credit_score', to='user.customer')),
            ],
        ),
    ]
