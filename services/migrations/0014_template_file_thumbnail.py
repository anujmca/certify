# Generated by Django 3.2.5 on 2021-09-01 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0013_certificate_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='file_thumbnail',
            field=models.FileField(blank=True, null=True, upload_to='templates/thumbnails/%Y/%m/%d/'),
        ),
    ]
