# Generated by Django 2.2.5 on 2020-06-01 13:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_name', models.CharField(max_length=200, verbose_name='Name')),
                ('card_type', models.CharField(choices=[('CTR', 'Creature'), ('ART', 'Artifact'), ('EMT', 'Enchantment'), ('PLW', 'Planeswalker'), ('INT', 'Instant'), ('SORC', 'Sorcery'), ('LAN', 'Land')], default='CTR', max_length=3, verbose_name='Card Type')),
                ('rarity', models.CharField(choices=[('COM', 'Common'), ('UCO', 'Uncommon'), ('RAR', 'Rare'), ('MYC', 'Mythic')], default='COM', max_length=3, verbose_name='Rarity')),
                ('expansion_set', models.CharField(max_length=75)),
                ('original_price', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('movement_price', models.FloatField()),
                ('current_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('historical_high', models.DecimalField(decimal_places=2, max_digits=10)),
                ('historical_high_date', models.DateField(auto_now_add=True, verbose_name='Highest Value Date')),
                ('quantity_owned', models.IntegerField(validators=[django.core.validators.MinValueValidator(0, 'Quantity owned must be greater or equal to 0')])),
            ],
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deck_name', models.CharField(max_length=50, verbose_name='Deck Name')),
                ('deck_format', models.CharField(choices=[('COM', 'Commander'), ('VNT', 'Vintage'), ('LEG', 'Legacy'), ('MOD', 'Modern'), ('PIO', 'Pioneer'), ('STD', 'Standard'), ('PAU', 'Pauper')], default='COM', max_length=3, verbose_name='Format')),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mtgdatabase.Card')),
            ],
        ),
        migrations.CreateModel(
            name='Decklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edit_time', models.DateTimeField(auto_now=True, verbose_name='Last edited')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mtgdatabase.Card')),
                ('deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mtgdatabase.Deck')),
                ('quantity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_quantity', to='mtgdatabase.Deck')),
            ],
        ),
    ]