# Generated by Django 4.0.5 on 2022-07-28 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_remove_checkout_checkout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='mobile',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='checkout',
            name='zip',
            field=models.CharField(max_length=300),
        ),
    ]
