# Generated by Django 5.0.3 on 2024-03-22 20:53

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyTransaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('currency', models.CharField(default='USD', max_length=3)),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
    ]
