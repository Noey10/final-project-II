# Generated by Django 4.1.4 on 2023-01-14 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_demo_model', '0013_alter_appliedscience_admission_grade_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appliedscience',
            old_name='english',
            new_name='langues',
        ),
        migrations.RenameField(
            model_name='healthscience',
            old_name='english',
            new_name='langues',
        ),
        migrations.RenameField(
            model_name='purescience',
            old_name='english',
            new_name='langues',
        ),
    ]
