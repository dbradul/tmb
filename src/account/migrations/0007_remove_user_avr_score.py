# Generated by Django 3.0.7 on 2020-07-14 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_user_avr_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avr_score',
        ),
    ]
