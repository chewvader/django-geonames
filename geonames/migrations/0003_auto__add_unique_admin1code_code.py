# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing index on 'Admin1Code', fields ['code']
        db.delete_index('geonames_admin1code', ['code'])

        # Adding unique constraint on 'Admin1Code', fields ['code']
        db.create_unique('geonames_admin1code', ['code'])

    def backwards(self, orm):
        # Removing unique constraint on 'Admin1Code', fields ['code']
        db.delete_unique('geonames_admin1code', ['code'])

        # Adding index on 'Admin1Code', fields ['code']
        db.create_index('geonames_admin1code', ['code'])

    models = {
        'geonames.admin1code': {
            'Meta': {'object_name': 'Admin1Code'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
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
            'Meta': {'ordering': "('name', 'country')", 'object_name': 'Geoname'},
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
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
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
