# Generated by Django 2.2.5 on 2020-07-02 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mtgdatabase', '0006_auto_20200702_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='collector_number',
            field=models.IntegerField(default=0),
        ),
    ]
