# Generated by Django 2.0 on 2017-12-20 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_title', models.CharField(max_length=250)),
                ('nextTrue', models.IntegerField(blank=True, null=True)),
                ('nextFalse', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
