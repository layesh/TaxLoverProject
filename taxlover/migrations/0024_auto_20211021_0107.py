# Generated by Django 3.2.6 on 2021-10-20 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxlover', '0023_auto_20211021_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advancetax',
            name='type',
            field=models.CharField(choices=[('CarAdvanceTax', 'Car Advance Tax'), ('Other', 'Other')], default='Other', max_length=20),
        ),
        migrations.AlterField(
            model_name='investment',
            name='type',
            field=models.CharField(choices=[('Shares/Debentures', 'Shares/Debentures'), ('Saving Certificate/Unit Certificate/Bond', 'Saving Certificate/Unit Certificate/Bond'), ('Prize Bond/Saving Scheme/FDR/DPS', 'Prize Bond/Saving Scheme/FDR/DPS'), ('Loans Given', 'Loans Given'), ('Other Investment', 'Other Investment')], default='Shares/Debentures', max_length=100),
        ),
    ]
