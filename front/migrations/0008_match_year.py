# Generated by Django 3.1.4 on 2020-12-02 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0007_auto_20201202_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='year',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
