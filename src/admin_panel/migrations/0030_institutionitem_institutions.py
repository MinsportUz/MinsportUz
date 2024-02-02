# Generated by Django 3.1.1 on 2023-10-26 07:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0029_carinfo_cars_cartypes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institutions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, null=True)),
                ('title_uz', models.CharField(max_length=500, null=True)),
                ('title_en', models.CharField(max_length=500, null=True)),
                ('title_ru', models.CharField(max_length=500, null=True)),
                ('title_sr', models.CharField(max_length=500, null=True)),
                ('url', models.TextField(blank=True, null=True)),
                ('slug', models.CharField(blank=True, max_length=25, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'institutions',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='InstitutionItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, null=True)),
                ('title_uz', models.CharField(max_length=500, null=True)),
                ('title_en', models.CharField(max_length=500, null=True)),
                ('title_ru', models.CharField(max_length=500, null=True)),
                ('title_sr', models.CharField(max_length=500, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='institutions')),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('address_uz', models.CharField(blank=True, max_length=500, null=True)),
                ('address_en', models.CharField(blank=True, max_length=500, null=True)),
                ('address_ru', models.CharField(blank=True, max_length=500, null=True)),
                ('address_sr', models.CharField(blank=True, max_length=500, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('number_of_practitioners', models.IntegerField(blank=True, default=0, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('sport_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_panel.sporttype')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_panel.staff')),
            ],
            options={
                'db_table': 'institution_item',
                'ordering': ['order', 'created_at'],
            },
        ),
    ]