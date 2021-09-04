# Generated by Django 3.2.5 on 2021-09-03 08:09

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('public', '0009_alter_publiccertificate_awardee'),
    ]

    operations = [
        migrations.CreateModel(
            name='FreeTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True, help_text='Datetime on which this record was created.')),
                ('updated_on', models.DateTimeField(auto_now=True, help_text='Datetime on which this record was last modified.', null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=400, null=True)),
                ('file', models.FileField(upload_to='templates/%Y/%m/%d/')),
                ('tokens', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, default=None, null=True, size=None)),
                ('file_thumbnail', models.FileField(blank=True, max_length=500, null=True, upload_to='templates/thumbnails/%Y/%m/%d/')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='freetemplate_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='freetemplate_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
