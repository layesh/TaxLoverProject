# Generated by Django 3.2.6 on 2021-10-01 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxlover', '0014_otherincome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otherincome',
            name='interest_from_mutual_fund_unit_fund',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
    ]
