# Generated by Django 4.1.4 on 2023-01-14 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_demo_model', '0012_delete_grades_delete_gradesinput'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appliedscience',
            name='admission_grade',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='appliedscience',
            name='art',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='appliedscience',
            name='career',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='appliedscience',
            name='english',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='appliedscience',
            name='gpa_year_1',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='appliedscience',
            name='hygiene',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='appliedscience',
            name='major',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='appliedscience',
            name='math',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='appliedscience',
            name='sci',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='appliedscience',
            name='society',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='appliedscience',
            name='status',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='appliedscience',
            name='thai',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='healthscience',
            name='admission_grade',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='healthscience',
            name='art',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='healthscience',
            name='career',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='healthscience',
            name='english',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='healthscience',
            name='gpa_year_1',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='healthscience',
            name='hygiene',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='healthscience',
            name='major',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='healthscience',
            name='math',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='healthscience',
            name='sci',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='healthscience',
            name='society',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='healthscience',
            name='status',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='healthscience',
            name='thai',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='purescience',
            name='admission_grade',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='purescience',
            name='art',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='purescience',
            name='career',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='purescience',
            name='english',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='purescience',
            name='gpa_year_1',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='purescience',
            name='hygiene',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='purescience',
            name='major',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='purescience',
            name='math',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='purescience',
            name='sci',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='purescience',
            name='society',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='purescience',
            name='status',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='purescience',
            name='thai',
            field=models.CharField(max_length=5),
        ),
    ]
