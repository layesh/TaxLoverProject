# Generated by Django 3.2.6 on 2021-10-20 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taxlover', '0022_agriculturalproperty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advancetax',
            name='type',
            field=models.CharField(choices=[('CarAdvanceTax', 'Car Advance Tax'), ('Other', 'Other')], max_length=20),
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('financial_year_beg', models.IntegerField(default=0)),
                ('financial_year_end', models.IntegerField(default=0)),
                ('type', models.CharField(choices=[('Shares/Debentures', 'Shares/Debentures'), ('Saving Certificate/Unit Certificate/Bond', 'Saving Certificate/Unit Certificate/Bond'), ('Prize Bond/Saving Scheme/FDR/DPS', 'Prize Bond/Saving Scheme/FDR/DPS'), ('Loans Given', 'Loans Given'), ('Other Investment', 'Other Investment')], max_length=100)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('tax_payer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxlover.taxpayer')),
            ],
        ),
    ]
