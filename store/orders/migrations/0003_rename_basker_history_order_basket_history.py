# Generated by Django 3.2.12 on 2023-02-01 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_rename_initiators_order_initiator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='basker_history',
            new_name='basket_history',
        ),
    ]
