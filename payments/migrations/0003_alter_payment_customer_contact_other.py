# Generated by Django 5.0.4 on 2024-08-02 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_rename_customer_contact_payment_customer_contact_india_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='customer_contact_other',
            field=models.CharField(default='', max_length=15),
        ),
    ]
