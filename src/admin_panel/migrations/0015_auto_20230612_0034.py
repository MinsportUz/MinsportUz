# Generated by Django 3.1.1 on 2023-06-11 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0014_auto_20230610_1915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='user',
        ),
        migrations.AddField(
            model_name='subscribers',
            name='fullname',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
