# Generated by Django 2.2 on 2019-05-30 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Topic'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Teacher'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='test',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Test'),
        ),
    ]
