# Generated by Django 2.2.7 on 2019-12-10 07:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sports', models.CharField(max_length=200)),
                ('image', models.ImageField(default='', upload_to='images')),
                ('slug', models.SlugField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('slug', models.SlugField(blank=True, default='')),
                ('description', models.TextField(max_length=1000)),
                ('image', models.ImageField(upload_to='news_images')),
                ('pub_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('city', models.CharField(default='city', max_length=20)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Played_Matches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team1', models.CharField(max_length=200)),
                ('team2', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, default='')),
                ('win1', models.DecimalField(decimal_places=2, max_digits=9)),
                ('win2', models.DecimalField(decimal_places=2, max_digits=9)),
                ('draw', models.DecimalField(decimal_places=2, max_digits=9)),
                ('game_time', models.DateTimeField()),
                ('game_end', models.DateTimeField(blank=True)),
                ('status', models.CharField(max_length=10)),
                ('winner', models.CharField(max_length=5)),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Categories')),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash', models.DecimalField(blank=True, decimal_places=2, default='', max_digits=10)),
                ('card_name', models.CharField(blank=True, default='', max_length=30)),
                ('card_number', models.CharField(blank=True, default='', max_length=19)),
                ('exp_date', models.CharField(blank=True, default='', max_length=30)),
                ('cvv', models.IntegerField(blank=True, default='')),
                ('payment_date', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Matches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team1', models.CharField(default='', max_length=200)),
                ('team2', models.CharField(default='', max_length=200)),
                ('slug', models.SlugField(blank=True, default='')),
                ('win1', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('win2', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('draw', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('game_time', models.DateTimeField()),
                ('game_end', models.DateTimeField(blank=True)),
                ('status', models.CharField(choices=[('COMPLETED', 'COMPLETED'), ('GOING', 'GOING'), ('EXPECTED', 'EXPECTED')], default='EXPECTED', max_length=10)),
                ('winner', models.CharField(choices=[('w1', 'w1'), ('w2', 'w2'), ('draw', 'draw'), ('UNKNOWN', 'UNKNOWN')], default='UNKNOWN', max_length=10)),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Categories')),
            ],
        ),
        migrations.CreateModel(
            name='Bets_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(default='', max_length=5)),
                ('coefficient', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('bet_cash', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('possible_win', models.DecimalField(decimal_places=2, default='', max_digits=9)),
                ('bet_date', models.DateTimeField()),
                ('winner', models.CharField(default='UNKNOWN', max_length=5)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Matches')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(default='', max_length=20)),
                ('choice', models.CharField(default='', max_length=5)),
                ('coefficient', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('bet_cash', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('possible_win', models.DecimalField(decimal_places=2, default='', max_digits=9)),
                ('bet_date', models.DateTimeField()),
                ('winner', models.CharField(default='UNKNOWN', max_length=5)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Matches')),
            ],
        ),
    ]
