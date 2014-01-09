from django.shortcuts import render_to_response,get_object_or_404
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,Http404
from okbadger.models import Issuer,Badge,Instance,Revocation,Claim
from okbadger.util import create_new_instance
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
    "revocationList": request.build_absolute_uri('../revocation')
    }
  return HttpResponse(json.dumps(data), content_type="application/json")

def badge(request,slug):
  i=get_object_or_404(Badge, slug=slug)
  data={
    "name": i.name,
    "description": i.description,
    "image": i.image,
    "criteria": request.build_absolute_uri('./%s/criteria'%i.slug),
    "issuer": request.build_absolute_uri('../issuer/%s'%i.issuer.slug),
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
      "badge": request.build_absolute_uri("../../%s"%i.badge.slug),
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
  """ Claim processing """
  i=get_object_or_404(Claim,id=id)
  # THIS IS UGLY - FIX!
  if i.recipient:
    i.multiple=False
  if request.method == "POST":
    if i.code:
      if i.code==request.POST["code"]:
        i.recipient = request.POST["recipient"]
    else:
      i.recipient = request.POST["recipient"]
  if not i.instance and i.recipient:
    i.instance=create_new_instance(i.badge,i.recipient,i.evidence)
  if not i.multiple:
    i.save()
  data={"claim": i,
    }
  if i.instance:
    data["assertion"]=request.build_absolute_uri("../badge/%s/instance/%s"%(i.badge.slug,
      i.instance.id))
  data.update(csrf(request))
  return render_to_response("claim.html",data)
