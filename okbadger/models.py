from django.db import models

# Create your models here.

class Issuer(models.Model):
  """ The issuer class - this represents the issuing organization """
  name = models.CharField(max_length=200)
  slug = models.CharField(max_length=100, unique=True)
  url = models.CharField(max_length=255)
  description = models.TextField()
  image = models.CharField(max_length=255)
  email = models.CharField(max_length=255)

  def __unicode__(self):
    return self.name

class Badge(models.Model):
  """ The badge description """
  slug = models.CharField(max_length=100,unique=True)
  name = models.CharField(max_length=500)
  description = models.TextField()
  image = models.CharField(max_length=500)
  criteria = models.TextField()
  issuer = models.ForeignKey('Issuer')
  
  def __unicode__(self):
    return self.name

class Instance(models.Model):
  """ An instance is a badge given to a person """
  badge=models.ForeignKey('Badge')
  recipient = models.CharField(max_length=500)
  evidence = models.CharField(max_length=500, null=True, blank=True)
  issuedOn = models.DateTimeField(auto_now=True)

  def __unicode__(self):
    return u"%s:%s"%(self.badge.name, self.id)

class Revocation(models.Model):
  """ Revocations of badges instanced """
  instance= models.ForeignKey('Instance')
  reason= models.CharField(max_length=500)

  def __unicode__(self):
    return "%s:%s"%(self.instance.id, self.reason)
  