# Generated by Django 3.2.5 on 2021-09-04 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='logo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='clients/<django.db.models.fields.CharField>/logo'),
        ),
    ]
