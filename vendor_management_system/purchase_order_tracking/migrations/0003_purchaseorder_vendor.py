# Generated by Django 4.2.7 on 2023-12-07 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_profile_management', '0002_alter_vendor_contact_details'),
        ('purchase_order_tracking', '0002_alter_purchaseorder_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='vendor',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='vendor_profile_management.vendor'),
        ),
    ]
