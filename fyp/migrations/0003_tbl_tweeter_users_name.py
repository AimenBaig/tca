# Generated by Django 3.0.3 on 2020-02-19 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fyp', '0002_auto_20200219_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_tweeter_users',
            name='name',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
