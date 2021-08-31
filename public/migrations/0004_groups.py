from django.db import migrations
from django.db import models, migrations
import services.utilities as utl


def apply_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.bulk_create([
        Group(name=utl.Groups.awardee),
    ])


def revert_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(
        name__in=[
            u'awardee',
        ]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('public', '0003_auto_20210829_2256'),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration)
    ]
