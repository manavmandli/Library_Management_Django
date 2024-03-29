# Generated by Django 4.2.11 on 2024-03-12 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0005_rename_student_transaction_member'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='rent_fee',
            new_name='charges',
        ),
        migrations.AlterField(
            model_name='book',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
