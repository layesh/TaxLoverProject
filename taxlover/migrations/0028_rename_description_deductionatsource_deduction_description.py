# Generated by Django 3.2.6 on 2021-10-24 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxlover', '0027_cashassets_electronicequipment_furniture_jewellery_otherassets_otherassetsreceipt_previousyearnetwea'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deductionatsource',
            old_name='description',
            new_name='deduction_description',
        ),
    ]