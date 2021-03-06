# Generated by Django 2.2.10 on 2020-02-15 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MenuPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('url_name', models.CharField(max_length=255)),
                ('depth', models.PositiveSmallIntegerField(default=0)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='points', to='core.Menu')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='core.MenuPoint')),
            ],
            options={
                'unique_together': {('menu', 'url_name')},
            },
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('power', models.PositiveSmallIntegerField()),
                ('ancestor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations_with_descendants', to='core.MenuPoint')),
                ('descendant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations_with_ancestors', to='core.MenuPoint')),
            ],
        ),
    ]
