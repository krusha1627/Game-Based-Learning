# Generated by Django 5.1.3 on 2024-12-28 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_word'),
    ]

    operations = [
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('img', models.CharField(max_length=255)),
                ('rating', models.FloatField()),
                ('color', models.CharField(max_length=50)),
                ('aosDelay', models.CharField(max_length=50)),
            ],
        ),
    ]
