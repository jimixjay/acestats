# Generated by Django 3.1.2 on 2020-12-01 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_num', models.IntegerField()),
                ('result', models.TextField()),
                ('best_of', models.IntegerField()),
                ('minutes', models.IntegerField()),
                ('round', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Nationality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('name', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='PlayerEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('name', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Surface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TourneyLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('name', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Tourney',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField()),
                ('surface', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='front.surface')),
                ('tourney_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front.tourneylevel')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('surname', models.TextField()),
                ('hand', models.TextField()),
                ('birthday', models.DateField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField()),
                ('nationality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='front.nationality')),
            ],
        ),
        migrations.CreateModel(
            name='MatchStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField()),
                ('seed', models.IntegerField()),
                ('aces', models.IntegerField()),
                ('double_faults', models.IntegerField()),
                ('service_points', models.IntegerField()),
                ('first_services', models.IntegerField()),
                ('first_services_won', models.IntegerField()),
                ('second_services_won', models.IntegerField()),
                ('service_game_won', models.IntegerField()),
                ('break_points_saved', models.IntegerField()),
                ('break_points_played', models.IntegerField()),
                ('rank', models.IntegerField()),
                ('rank_points', models.IntegerField()),
                ('is_winner', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField()),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front.match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front.player')),
                ('player_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front.playerentry')),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='tourney',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='front.tourney'),
        ),
    ]
