# Generated by Django 3.0.7 on 2020-07-14 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200701_1445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avr_score',
        ),
        migrations.AddField(
            model_name='user',
            name='correct_answers',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='total_questions',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
    ]
