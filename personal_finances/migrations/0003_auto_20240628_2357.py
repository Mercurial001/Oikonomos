# Generated by Django 3.2 on 2024-06-28 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('personal_finances', '0002_auto_20240628_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalfund',
            name='removed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personalreceivedfund',
            name='fund',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='personal_finances.personalfund'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='RemovedPersonalFinanceData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('object_id', models.IntegerField()),
                ('amount', models.FloatField(blank=True, null=True)),
                ('date', models.DateField()),
                ('date_time', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalFundAdded',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('date', models.DateField()),
                ('date_time', models.DateTimeField()),
                ('fund', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_finances.personalfund')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDebts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('amount', models.FloatField()),
                ('date', models.DateField()),
                ('date_time', models.DateTimeField()),
                ('paid', models.BooleanField(default=False)),
                ('paid_amount', models.FloatField(blank=True, null=True)),
                ('date_paid', models.DateField(blank=True, null=True)),
                ('date_time_paid', models.DateTimeField(blank=True, null=True)),
                ('fund', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='personal_finances.personalfund')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
