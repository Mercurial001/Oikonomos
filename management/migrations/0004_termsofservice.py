# Generated by Django 3.2 on 2024-07-09 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_privacypolicy'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermsOfService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('statement', models.TextField()),
                ('date_updated', models.DateField()),
                ('date_time_updated', models.DateTimeField()),
            ],
        ),
    ]
