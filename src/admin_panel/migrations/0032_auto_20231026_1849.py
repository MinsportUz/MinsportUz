# Generated by Django 3.1.1 on 2023-10-26 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0031_institutionitem_institution'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutionitem',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='institutionitem',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
