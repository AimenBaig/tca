# Generated by Django 3.0.3 on 2020-03-01 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fyp', '0009_auto_20200301_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_analysis',
            name='analysis_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
