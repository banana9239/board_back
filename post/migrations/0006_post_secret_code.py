# Generated by Django 5.1.1 on 2025-01-18 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_alter_postcomment_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='secret_code',
            field=models.CharField(blank=True, default='', max_length=60, null=True),
        ),
    ]
