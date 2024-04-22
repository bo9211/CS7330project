# Generated by Django 5.0.4 on 2024-04-18 01:19

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('level', models.CharField(max_length=50)),
            ],
            options={
                'unique_together': {('name', 'level')},
            },
        ),
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('objective_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=120, unique=True)),
                ('description', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university.course')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_id', models.CharField(max_length=3, validators=[django.core.validators.MaxValueValidator(999), django.core.validators.MinValueValidator(100)])),
                ('semester', models.CharField(choices=[('Spring', 'Spring'), ('Summer', 'Summer'), ('Fall', 'Fall')], max_length=6)),
                ('year', models.IntegerField()),
                ('enrolled_stu_num', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='university.course')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='university.instructor')),
            ],
            options={
                'unique_together': {('course', 'section_id', 'semester', 'year')},
            },
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('evaluate_id', models.AutoField(primary_key=True, serialize=False)),
                ('method', models.CharField(max_length=255)),
                ('levelA_stu_num', models.IntegerField()),
                ('levelB_stu_num', models.IntegerField()),
                ('levelC_stu_num', models.IntegerField()),
                ('levelF_stu_num', models.IntegerField()),
                ('improvement_suggestions', models.TextField(blank=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university.course')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university.section')),
            ],
        ),
        migrations.CreateModel(
            name='DegreeCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_core', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university.course')),
                ('degree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university.degree')),
            ],
            options={
                'unique_together': {('degree', 'course')},
            },
        ),
        migrations.CreateModel(
            name='EvaluatorObjective',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evaluation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university.evaluation')),
                ('objective', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university.objective')),
            ],
            options={
                'unique_together': {('evaluation', 'objective')},
            },
        ),
    ]
