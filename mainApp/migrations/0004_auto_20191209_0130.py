# Generated by Django 2.2.7 on 2019-12-08 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0003_auto_20191209_0129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='card_number',
            field=models.CharField(blank=True, default='', max_length=19),
        ),
    ]
