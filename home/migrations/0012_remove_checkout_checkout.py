# Generated by Django 4.0.5 on 2022-07-28 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_checkout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkout',
            name='checkout',
        ),
    ]
