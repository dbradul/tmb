# Generated by Django 3.0.5 on 2020-06-14 07:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testsuite', '0006_auto_20200614_0658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='num_variant_limit',
            field=models.PositiveSmallIntegerField(default=3, validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(6)]),
        ),
    ]
