# Generated by Django 4.0.6 on 2022-07-30 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flights',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
