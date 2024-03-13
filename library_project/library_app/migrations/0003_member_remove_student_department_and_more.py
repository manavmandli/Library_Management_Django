# Generated by Django 4.2.11 on 2024-03-12 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library_app', '0002_author_department_student_remove_book_title_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=120)),
                ('member_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='student',
            name='department',
        ),
        migrations.RemoveField(
            model_name='student',
            name='student_id',
        ),
        migrations.DeleteModel(
            name='Department',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_app.member'),
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]