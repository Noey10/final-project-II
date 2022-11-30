# Generated by Django 4.1.3 on 2022-11-24 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=30)),
                ('plan_highschool', models.CharField(max_length=50)),
                ('highschool_grade', models.CharField(max_length=50)),
                ('professional_grade', models.CharField(max_length=50)),
                ('compulsory_pro_grade', models.CharField(max_length=50)),
                ('select_vocation_grade', models.CharField(max_length=50)),
                ('compulsory_elective_1', models.CharField(max_length=50)),
                ('compulsory_elective_2', models.CharField(max_length=50)),
                ('foreign_language_grade', models.CharField(max_length=50)),
                ('thai_grade', models.CharField(max_length=50)),
                ('avg_grade', models.CharField(max_length=50)),
                ('result_predict', models.CharField(max_length=50)),
                ('predict_at', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
