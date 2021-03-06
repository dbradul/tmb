# Generated by Django 3.0.5 on 2020-06-12 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestSuite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField(blank=True, max_length=1024, null=True)),
                ('level', models.PositiveSmallIntegerField(choices=[(1, 'Basic'), (2, 'Middle'), (3, 'Advanced')], default=2)),
            ],
        ),
    ]
