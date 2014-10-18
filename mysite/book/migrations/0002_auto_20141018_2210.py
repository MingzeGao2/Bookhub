# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ISBN', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=200)),
                ('amount', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_title', models.CharField(max_length=200)),
                ('semester', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Need',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('intention', models.CharField(max_length=200)),
                ('book', models.ForeignKey(to='book.Book')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Require',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.ForeignKey(to='book.Course')),
                ('required_book', models.ForeignKey(to='book.Book')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='Users',
            new_name='User',
        ),
        migrations.AddField(
            model_name='registration',
            name='student',
            field=models.ForeignKey(to='book.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='registration',
            name='to_course',
            field=models.ForeignKey(to='book.Course'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='need',
            name='user',
            field=models.ForeignKey(to='book.User'),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='user',
            old_name='Users_name',
            new_name='User_name',
        ),
    ]
