# Generated by Django 4.1.3 on 2023-08-10 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0020_alter_staticdata_content_alter_staticdata_content_en_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staticdata',
            name='main_url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='staticdata',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
