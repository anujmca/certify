# Generated by Django 3.2.5 on 2021-08-31 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0011_auto_20210831_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='awardee_public_id',
            field=models.BigIntegerField(blank=True, default=None, null=True),
        ),
    ]
