# Generated by Django 5.0.2 on 2024-03-23 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0003_studymaterials'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_materials',
            field=models.BooleanField(default=False),
        ),
    ]
