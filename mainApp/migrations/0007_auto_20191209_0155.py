# Generated by Django 2.2.7 on 2019-12-08 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0006_bets_possible_win'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bets',
            name='possible_win',
            field=models.DecimalField(decimal_places=2, default='', max_digits=9),
        ),
    ]
