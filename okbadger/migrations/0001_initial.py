# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Issuer'
        db.create_table(u'okbadger_issuer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'okbadger', ['Issuer'])

        # Adding model 'Badge'
        db.create_table(u'okbadger_badge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('criteria', self.gf('django.db.models.fields.TextField')()),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['okbadger.Issuer'])),
        ))
        db.send_create_signal(u'okbadger', ['Badge'])

        # Adding model 'Instance'
        db.create_table(u'okbadger_instance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('badge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['okbadger.Badge'])),
            ('recipient', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('evidence', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('issuedOn', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'okbadger', ['Instance'])

        # Adding model 'Revocation'
        db.create_table(u'okbadger_revocation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['okbadger.Instance'])),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'okbadger', ['Revocation'])

        # Adding model 'Claim'
        db.create_table(u'okbadger_claim', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('badge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['okbadger.Badge'])),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['okbadger.Instance'], null=True, blank=True)),
            ('recipient', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('evidence', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('multiple', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal(u'okbadger', ['Claim'])

        # Adding model 'Application'
        db.create_table(u'okbadger_application', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'okbadger', ['Application'])

        # Adding M2M table for field badges on 'Application'
        m2m_table_name = db.shorten_name(u'okbadger_application_badges')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('application', models.ForeignKey(orm[u'okbadger.application'], null=False)),
            ('badge', models.ForeignKey(orm[u'okbadger.badge'], null=False))
        ))
        db.create_unique(m2m_table_name, ['application_id', 'badge_id'])


    def backwards(self, orm):
        # Deleting model 'Issuer'
        db.delete_table(u'okbadger_issuer')

        # Deleting model 'Badge'
        db.delete_table(u'okbadger_badge')

        # Deleting model 'Instance'
        db.delete_table(u'okbadger_instance')

        # Deleting model 'Revocation'
        db.delete_table(u'okbadger_revocation')

        # Deleting model 'Claim'
        db.delete_table(u'okbadger_claim')

        # Deleting model 'Application'
        db.delete_table(u'okbadger_application')

        # Removing M2M table for field badges on 'Application'
        db.delete_table(db.shorten_name(u'okbadger_application_badges'))


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
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
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
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
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