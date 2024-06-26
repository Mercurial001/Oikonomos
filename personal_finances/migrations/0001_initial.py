# Generated by Django 3.2 on 2024-06-26 10:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalExpense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('amount', models.IntegerField()),
                ('date', models.DateField()),
                ('date_time', models.DateTimeField()),
                ('document', models.ImageField(blank=True, null=True, upload_to='expenses/')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalReceivedFund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('amount', models.IntegerField()),
                ('date', models.DateField()),
                ('date_time', models.DateTimeField()),
                ('document', models.ImageField(blank=True, null=True, upload_to='funds/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalNetWorth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalFundExpenditure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('amount', models.IntegerField()),
                ('date', models.DateField()),
                ('date_time', models.DateTimeField()),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_finances.personalexpense')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalFund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('amount', models.IntegerField()),
                ('date', models.DateField()),
                ('date_time', models.DateTimeField()),
                ('depleted_date', models.DateField(blank=True, null=True)),
                ('depleted_date_time', models.DateTimeField(blank=True, null=True)),
                ('depleted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='personalexpense',
            name='fund',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_finances.personalfund'),
        ),
        migrations.AddField(
            model_name='personalexpense',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='personal_expense', to=settings.AUTH_USER_MODEL),
        ),
    ]