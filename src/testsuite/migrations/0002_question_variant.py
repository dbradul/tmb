# Generated by Django 3.0.5 on 2020-06-12 09:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testsuite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=64)),
                ('description', models.TextField(blank=True, max_length=512, null=True)),
                ('num_variant_limit', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(6)])),
                ('test_suite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='testsuite.TestSuite')),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=64)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variant', to='testsuite.Question')),
            ],
        ),
    ]
