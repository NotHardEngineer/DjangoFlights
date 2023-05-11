# Generated by Django 4.2 on 2023-04-19 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flights',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=255)),
                ('time', models.DateTimeField()),
                ('airport_iata', models.CharField(max_length=3)),
                ('is_depart', models.BooleanField()),
                ('plane_type', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]