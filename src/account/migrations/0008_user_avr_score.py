# Generated by Django 3.0.7 on 2020-07-14 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_remove_user_avr_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avr_score',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6),
        ),
    ]
