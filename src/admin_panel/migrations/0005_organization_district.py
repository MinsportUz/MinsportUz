# Generated by Django 3.1.1 on 2023-04-28 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0004_auto_20230428_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_panel.district'),
        ),
    ]