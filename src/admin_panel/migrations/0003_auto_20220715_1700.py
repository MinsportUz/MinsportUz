# Generated by Django 3.1.1 on 2022-07-15 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0002_docs_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docs',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='file'),
        ),
        migrations.AlterField(
            model_name='docs',
            name='law',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='docs',
            name='law_en',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='docs',
            name='law_ru',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='docs',
            name='law_sr',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='docs',
            name='law_uz',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
