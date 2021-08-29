# Generated by Django 3.2.6 on 2021-08-29 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxlover', '0010_rename_document_document_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary',
            name='arrear_pay',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='salary',
            name='bengali_new_year_bonus',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='salary',
            name='dearness_allowance',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='salary',
            name='deemed_free_accommodation',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='salary',
            name='deemed_income_transport',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='salary',
            name='festival_allowance',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='salary',
            name='honorarium_or_reward',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='salary',
            name='income_from_pf_and_saf',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='salary',
            name='interest_accrued_from_pf',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='salary',
            name='leave_encashment',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='salary',
            name='other_allowances',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='salary',
            name='others',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='salary',
            name='overtime_allowance',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='salary',
            name='pension',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='salary',
            name='special_pay',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='salary',
            name='support_staff_allowance',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='salary',
            name='total_bonus',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='salary',
            name='ait',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='salary',
            name='basic',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='salary',
            name='conveyance',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='salary',
            name='employees_contribution_to_pf',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='salary',
            name='employers_contribution_to_pf',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='salary',
            name='festival_bonus',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='salary',
            name='house_rent',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='salary',
            name='lfa',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='salary',
            name='medical',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='salary',
            name='other_bonus',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
    ]