# Generated by Django 3.1.7 on 2021-04-22 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blackList', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmodel',
            name='date',
            field=models.DateTimeField(),
        ),
    ]