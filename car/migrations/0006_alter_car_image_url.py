# Generated by Django 4.2.2 on 2023-07-07 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0005_car_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='image_url',
            field=models.URLField(max_length=2083, null=True),
        ),
    ]
