# Generated by Django 2.2.6 on 2020-01-20 20:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0006_auto_20200120_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user_reaction',
            field=models.ManyToManyField(blank=True, related_name='reaction', to=settings.AUTH_USER_MODEL),
        ),
    ]
