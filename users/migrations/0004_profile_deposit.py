# Generated by Django 3.2 on 2022-09-24 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220924_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='deposit',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
