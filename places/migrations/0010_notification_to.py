# Generated by Django 2.2 on 2022-02-26 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0009_order_created_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='to',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='places.Customer'),
            preserve_default=False,
        ),
    ]
