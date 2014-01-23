# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Issuer.slug'
        db.alter_column(u'okbadger_issuer', 'slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50))
        # Adding index on 'Issuer', fields ['slug']
        db.create_index(u'okbadger_issuer', ['slug'])


        # Changing field 'Badge.slug'
        db.alter_column(u'okbadger_badge', 'slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50))
        # Adding index on 'Badge', fields ['slug']
        db.create_index(u'okbadger_badge', ['slug'])


    def backwards(self, orm):
        # Removing index on 'Badge', fields ['slug']
        db.delete_index(u'okbadger_badge', ['slug'])

        # Removing index on 'Issuer', fields ['slug']
        db.delete_index(u'okbadger_issuer', ['slug'])


        # Changing field 'Issuer.slug'
        db.alter_column(u'okbadger_issuer', 'slug', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True))

        # Changing field 'Badge.slug'
        db.alter_column(u'okbadger_badge', 'slug', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True))

    models = {
        u'okbadger.application': {
            'Meta': {'object_name': 'Application'},
            'badges': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['okbadger.Badge']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'okbadger.badge': {
            'Meta': {'object_name': 'Badge'},
            'criteria': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['okbadger.Issuer']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'okbadger.claim': {
            'Meta': {'object_name': 'Claim'},
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['okbadger.Badge']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'evidence': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['okbadger.Instance']", 'null': 'True', 'blank': 'True'}),
            'multiple': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipient': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'okbadger.instance': {
            'Meta': {'object_name': 'Instance'},
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['okbadger.Badge']"}),
            'evidence': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuedOn': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'recipient': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'okbadger.issuer': {
            'Meta': {'object_name': 'Issuer'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'okbadger.revocation': {
            'Meta': {'object_name': 'Revocation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['okbadger.Instance']"}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['okbadger']