# Generated by Django 2.2.6 on 2020-03-04 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20200222_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dislk_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]