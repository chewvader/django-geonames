# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin1Code',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=58)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Admin2Code',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('code', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=46)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Alternate',
            fields=[
                ('alternateid', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('isolanguage', models.CharField(max_length=7)),
                ('variant', models.CharField(db_index=True, max_length=200)),
                ('preferred', models.BooleanField(db_index=True, default=None)),
                ('short', models.BooleanField(default=None)),
                ('colloquial', models.BooleanField(default=None)),
                ('historic', models.BooleanField(default=None)),
            ],
            options={
                'ordering': ('-preferred',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Geoname',
            fields=[
                ('geonameid', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('asciiname', models.CharField(db_index=True, max_length=200)),
                ('alternates', models.TextField(blank=True)),
                ('fclass', models.CharField(db_index=True, max_length=1)),
                ('fcode', models.CharField(db_index=True, max_length=10)),
                ('country', models.CharField(blank=True, db_index=True, max_length=2)),
                ('cc2', models.CharField(blank=True, verbose_name='Alternate Country Code', max_length=100)),
                ('admin1', models.CharField(blank=True, db_index=True, max_length=20)),
                ('admin2', models.CharField(blank=True, db_index=True, max_length=80)),
                ('admin3', models.CharField(blank=True, db_index=True, max_length=20)),
                ('admin4', models.CharField(blank=True, db_index=True, max_length=20)),
                ('population', models.BigIntegerField(db_index=True)),
                ('elevation', models.IntegerField(db_index=True)),
                ('topo', models.IntegerField(db_index=True)),
                ('timezone', models.CharField(blank=True, max_length=40)),
                ('moddate', models.DateField(verbose_name='Date of Last Modification')),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326, geography=True, null=True)),
            ],
            options={
                'ordering': ('name', 'country'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostalCode',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('countrycode', models.CharField(max_length=2)),
                ('postalcode', models.CharField(max_length=20)),
                ('placename', models.CharField(max_length=200)),
                ('admin1name', models.CharField(max_length=200)),
                ('admin1code', models.CharField(max_length=20)),
                ('admin2name', models.CharField(max_length=200)),
                ('admin2code', models.CharField(max_length=80)),
                ('admin3name', models.CharField(max_length=200)),
                ('admin3code', models.CharField(max_length=20)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('accuracy', models.SmallIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeZone',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('tzid', models.CharField(max_length=30)),
                ('gmt_offset', models.FloatField()),
                ('dst_offset', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='alternate',
            name='geonameid',
            field=models.ForeignKey(to='geonames.Geoname', related_name='alternate_names'),
            preserve_default=True,
        ),
    ]
