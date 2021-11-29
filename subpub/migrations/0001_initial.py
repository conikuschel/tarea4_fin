# Generated by Django 3.2.9 on 2021-11-29 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=100)),
                ('banco_origen', models.IntegerField()),
                ('cuenta_origen', models.IntegerField()),
                ('banco_destino', models.IntegerField()),
                ('cuenta_destino', models.IntegerField()),
                ('monto', models.IntegerField()),
                ('message_id', models.CharField(max_length=100)),
                ('fecha', models.CharField(max_length=100)),
            ],
        ),
    ]
