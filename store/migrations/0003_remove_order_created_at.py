# Generated by Django 4.2.16 on 2024-10-20 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_order_date_order_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='created_at',
        ),
    ]
