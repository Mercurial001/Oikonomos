# Generated by Django 3.2 on 2024-07-03 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_finances', '0004_personalfundexpenditure_net_worth_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalexpense',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='personalfund',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='personalfundexpenditure',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='personalnetworth',
            name='amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='personalreceivedfund',
            name='amount',
            field=models.FloatField(),
        ),
    ]