# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Admin1Code'
        db.create_table('geonames_admin1code', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=58)),
        ))
        db.send_create_signal('geonames', ['Admin1Code'])

        # Adding model 'Admin2Code'
        db.create_table('geonames_admin2code', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=46)),
        ))
        db.send_create_signal('geonames', ['Admin2Code'])

        # Adding model 'TimeZone'
        db.create_table('geonames_timezone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tzid', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('gmt_offset', self.gf('django.db.models.fields.FloatField')()),
            ('dst_offset', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('geonames', ['TimeZone'])

        # Adding model 'Geoname'
        db.create_table('geonames_geoname', (
            ('geonameid', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('alternates', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('fclass', self.gf('django.db.models.fields.CharField')(max_length=1, db_index=True)),
            ('fcode', self.gf('django.db.models.fields.CharField')(max_length=10, db_index=True)),
            ('country', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=2, blank=True)),
            ('cc2', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('admin1', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=20, blank=True)),
            ('admin2', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=80, blank=True)),
            ('admin3', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=20, blank=True)),
            ('admin4', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=20, blank=True)),
            ('population', self.gf('django.db.models.fields.BigIntegerField')(db_index=True)),
            ('elevation', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('topo', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('moddate', self.gf('django.db.models.fields.DateField')()),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True)),
        ))
        db.send_create_signal('geonames', ['Geoname'])

        # Adding model 'Alternate'
        db.create_table('geonames_alternate', (
            ('alternateid', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, primary_key=True)),
            ('geoname', self.gf('django.db.models.fields.related.ForeignKey')(related_name='alternate_names', to=orm['geonames.Geoname'])),
            ('isolanguage', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('variant', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('preferred', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('short', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('geonames', ['Alternate'])

        # Adding model 'PostalCode'
        db.create_table('geonames_postalcode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('countrycode', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('postalcode', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('placename', self.gf('django.db.models.fields.CharField')(max_length=180)),
            ('admin1name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('admin1code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('admin2name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('admin2code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('admin3name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('admin3code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('accuracy', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('geonames', ['PostalCode'])

    def backwards(self, orm):
        # Deleting model 'Admin1Code'
        db.delete_table('geonames_admin1code')

        # Deleting model 'Admin2Code'
        db.delete_table('geonames_admin2code')

        # Deleting model 'TimeZone'
        db.delete_table('geonames_timezone')

        # Deleting model 'Geoname'
        db.delete_table('geonames_geoname')

        # Deleting model 'Alternate'
        db.delete_table('geonames_alternate')

        # Deleting model 'PostalCode'
        db.delete_table('geonames_postalcode')

    models = {
        'geonames.admin1code': {
            'Meta': {'object_name': 'Admin1Code'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '58'})
        },
        'geonames.admin2code': {
            'Meta': {'object_name': 'Admin2Code'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '46'})
        },
        'geonames.alternate': {
            'Meta': {'ordering': "('-preferred',)", 'object_name': 'Alternate'},
            'alternateid': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'geoname': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alternate_names'", 'to': "orm['geonames.Geoname']"}),
            'isolanguage': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'preferred': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'short': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'variant': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'})
        },
        'geonames.geoname': {
            'Meta': {'object_name': 'Geoname'},
            'admin1': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'blank': 'True'}),
            'admin2': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '80', 'blank': 'True'}),
            'admin3': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'blank': 'True'}),
            'admin4': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'blank': 'True'}),
            'alternates': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'cc2': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '2', 'blank': 'True'}),
            'elevation': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'fclass': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            'fcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'geonameid': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'moddate': ('django.db.models.fields.DateField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'geography': 'True'}),
            'population': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'topo': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        'geonames.postalcode': {
            'Meta': {'object_name': 'PostalCode'},
            'accuracy': ('django.db.models.fields.SmallIntegerField', [], {}),
            'admin1code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'admin1name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'admin2code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'admin2name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'admin3code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'admin3name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'countrycode': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'placename': ('django.db.models.fields.CharField', [], {'max_length': '180'}),
            'postalcode': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'geonames.timezone': {
            'Meta': {'object_name': 'TimeZone'},
            'dst_offset': ('django.db.models.fields.FloatField', [], {}),
            'gmt_offset': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tzid': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['geonames']
