# Generated by Django 3.1.1 on 2023-08-11 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0021_alter_staticdata_main_url_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(blank=True, max_length=100, null=True)),
                ('region', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('browser', models.CharField(blank=True, max_length=100, null=True)),
                ('os', models.CharField(blank=True, max_length=100, null=True)),
                ('device', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'visitors',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='VisitorLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.visitor')),
            ],
            options={
                'db_table': 'visitor_logs',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='visitorlog',
            index=models.Index(fields=['created_at'], name='visitor_log_created_5c5fc2_idx'),
        ),
    ]
