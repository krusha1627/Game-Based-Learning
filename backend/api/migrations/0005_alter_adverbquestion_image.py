# Generated by Django 5.1.3 on 2025-02-04 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_adverbquestion_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adverbquestion',
            name='image',
            field=models.URLField(),
        ),
    ]
