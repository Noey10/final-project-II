# Generated by Django 4.1.3 on 2022-12-06 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_demo_model', '0005_alter_grades_admission_grade_alter_grades_art_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grades',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
