# Generated by Django 3.1.7 on 2021-04-22 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blackList', '0003_auto_20210422_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmodel',
            name='date',
            field=models.CharField(max_length=30),
        ),
    ]
