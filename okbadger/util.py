from okbadger.models import Instance,Claim
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import json

def create_new_instance(badge,recipient,evidence=None):
  """ Creates a new instance or returns an old instance if it already
  exists """
  try:
    i=Instance.objects.get(badge=badge,recipient=recipient)
  except ObjectDoesNotExist:  
    i=Instance()
    i.badge=badge
    i.recipient=recipient
    i.evidence=evidence
    i.save()
  return i

def json_response(data):
  rs=HttpResponse(json.dumps(data),content_type="application/json")
  rs['Access-Control-Allow-Origin']="*"
  return rs

def create_or_return_claim(badge,recipient,evidence=None):
  try:
    c=Claim.objects.get(badge=badge,recipient=recipient)
    if not c.instance:
      c.instance=create_new_instance(badge,recipient,evidence)
  except ObjectDoesNotExist:
    c=Claim()
    c.badge=badge
    c.recipient=recipient
    c.instance=create_new_instance(badge,recipient,evidence)
    c.save()
  return c
