# Generated by Django 4.2.11 on 2024-03-11 19:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=350)),
                ('description', models.CharField(max_length=450)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=120)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_app.department')),
                ('student_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='book',
            name='title',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='issue_date',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='member',
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.CharField(default=1, max_length=220),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(default=0, upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='name',
            field=models.CharField(default=1, max_length=350),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='issued',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='issued_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='returned',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='return_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Member',
        ),
        migrations.AddField(
            model_name='transaction',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='library_app.student'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_app.author'),
        ),
    ]
