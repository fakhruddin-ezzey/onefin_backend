# Generated by Django 4.1.7 on 2023-10-10 18:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('collection_app', '0005_delete_userjwtgeneratedtoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercollections',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('cec340f0-5b20-4924-aa92-48c309ead2ff'), primary_key=True, serialize=False),
        ),
    ]
