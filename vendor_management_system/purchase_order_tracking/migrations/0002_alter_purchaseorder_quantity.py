# Generated by Django 4.2.7 on 2023-12-03 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order_tracking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]