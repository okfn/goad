from django.shortcuts import render_to_response,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,Http404
from okbadger.models import Issuer,Badge,Instance,Revocation,Claim
import json
import markdown
import hashlib
import time


def issuer(request,slug=None):
  i=get_object_or_404(Issuer, slug=slug)
  data={"name": i.name,
    "url": i.url,
    "image": i.image,
    "description": i.description,
    "email": i.email,
    "revocationList": "http://%s/revocation"%request.get_host() }
  return HttpResponse(json.dumps(data), content_type="application/json")

def badge(request,slug):
  i=get_object_or_404(Badge, slug=slug)
  data={
    "name": i.name,
    "description": i.description,
    "image": i.image,
    "criteria": "http://%s/badge/%s/criteria"%(request.get_host(),i.slug),
    "issuer": "http://%s/issuer/%s"%(request.get_host(),i.issuer.slug),
    }
  return HttpResponse(json.dumps(data), content_type="application/json")

def badge_criteria(request,slug):
  i=get_object_or_404(Badge, slug=slug)
  return HttpResponse(markdown.markdown(i.criteria))

def instance(request,slug,id):
  i=get_object_or_404(Instance,id=id)
  try:
    r=Revocation.objects.get(instance=i)
    raise Http404
  except ObjectDoesNotExist:  
    data={
      "uid": "%s"%i.id,
      "recipient": {
        "identity":"sha256$%s"%(hashlib.sha256(i.recipient).hexdigest()),
        "hashed": True,
        "type": "email",
        },
      "badge": "http://%s/badge/%s"%(request.get_host(),i.badge.slug),
      "verify": {
        "type":"hosted",
        "url": request.build_absolute_uri()
        },
      "issuedOn":time.mktime(i.issuedOn.timetuple()),
      "evidence": i.evidence,
  
      }
    return HttpResponse(json.dumps(data), content_type="application/json")

def revocation(request):
  r=Revocation.objects.all()
  data=dict(((i.instance.id,i.reason) for i in r))
  return HttpResponse(json.dumps(data), content_type="application/json")


def claim(request,id=None):
  i=get_object_or_404(Claim,id=id)
  data={}
  return render_to_response("claim.html",data)
