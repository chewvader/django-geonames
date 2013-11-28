# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Alternate'
        db.delete_table(u'geonames_alternate')

        # Deleting model 'Admin1Code'
        db.delete_table(u'geonames_admin1code')

        # Deleting model 'Admin2Code'
        db.delete_table(u'geonames_admin2code')

        # Deleting model 'Geoname'
        db.delete_table(u'geonames_geoname')

        # Deleting model 'PostalCode'
        db.delete_table(u'geonames_postalcode')

        # Deleting model 'TimeZone'
        db.delete_table(u'geonames_timezone')

    def backwards(self, orm):
        # Adding model 'Alternate'
        db.create_table(u'geonames_alternate', (
            ('isolanguage', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('short', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('variant', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('alternateid', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, primary_key=True)),
            ('preferred', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('geoname', self.gf('django.db.models.fields.related.ForeignKey')(related_name='alternate_names', to=orm['geonames.Geoname'])),
        ))
        db.send_create_signal('geonames', ['Alternate'])

        # Adding model 'Admin1Code'
        db.create_table(u'geonames_admin1code', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=10, unique=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=58)),
        ))
        db.send_create_signal('geonames', ['Admin1Code'])

        # Adding model 'Admin2Code'
        db.create_table(u'geonames_admin2code', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=46)),
        ))
        db.send_create_signal('geonames', ['Admin2Code'])

        # Adding model 'Geoname'
        db.create_table(u'geonames_geoname', (
            ('fclass', self.gf('django.db.models.fields.CharField')(max_length=1, db_index=True)),
            ('admin2', self.gf('django.db.models.fields.CharField')(blank=True, max_length=80, db_index=True)),
            ('elevation', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True)),
            ('geonameid', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, primary_key=True)),
            ('country', self.gf('django.db.models.fields.CharField')(blank=True, max_length=2, db_index=True)),
            ('fcode', self.gf('django.db.models.fields.CharField')(max_length=10, db_index=True)),
            ('cc2', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('admin1', self.gf('django.db.models.fields.CharField')(blank=True, max_length=20, db_index=True)),
            ('admin3', self.gf('django.db.models.fields.CharField')(blank=True, max_length=20, db_index=True)),
            ('topo', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('admin4', self.gf('django.db.models.fields.CharField')(blank=True, max_length=20, db_index=True)),
            ('moddate', self.gf('django.db.models.fields.DateField')()),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('population', self.gf('django.db.models.fields.BigIntegerField')(db_index=True)),
            ('searchable_name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=200, null=True, db_index=True)),
            ('alternates', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('geonames', ['Geoname'])

        # Adding model 'PostalCode'
        db.create_table(u'geonames_postalcode', (
            ('admin1name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('admin1code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('postalcode', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('admin3code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('admin2name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('placename', self.gf('django.db.models.fields.CharField')(max_length=180)),
            ('countrycode', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('admin2code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('admin3name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('accuracy', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('geonames', ['PostalCode'])

        # Adding model 'TimeZone'
        db.create_table(u'geonames_timezone', (
            ('gmt_offset', self.gf('django.db.models.fields.FloatField')()),
            ('tzid', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dst_offset', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('geonames', ['TimeZone'])

    models = {
        
    }

    complete_apps = ['geonames']