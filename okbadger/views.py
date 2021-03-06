import json
import markdown
import hashlib
import time
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.db import connection
from okbadger.models import *
from okbadger.util import create_new_instance, json_response
from okbadger.util import create_or_return_claim


def issuer(request, slug=None):
    i = get_object_or_404(Issuer, slug=slug)
    data = {"name": i.name,
            "url": i.url,
            "image": i.image,
            "description": i.description,
            "email": i.email,
            "contact": i.email,
            "revocationList": request.build_absolute_uri('../revocation')
            }
    return json_response(data)


def badge(request, slug):
    i = get_object_or_404(Badge, slug=slug)
    data = {
        "name": i.name,
        "description": i.description,
        "image": i.image,
        "criteria": request.build_absolute_uri('./%s/criteria' % i.slug),
        "issuer": request.build_absolute_uri('../issuer/%s' % i.issuer.slug),
        }
    return json_response(data)


def badge_criteria(request, slug):
    i = get_object_or_404(Badge, slug=slug)
    data = {
        "badge": i,
        "criteria": markdown.markdown(i.criteria)
        }
    return render_to_response("criteria.html", data)


def instance(request, slug, id):
    i = get_object_or_404(Instance, id=id)
    try:
        r = Revocation.objects.get(instance=i)
        raise Http404
    except ObjectDoesNotExist:
        data = {
            "uid": "%s" % i.id,
            "recipient": {
                "identity": "sha256$%s" % (
                    hashlib.sha256(i.recipient).hexdigest()),
                "hashed": True,
                "type": "email",
                },
            "badge": request.build_absolute_uri("../../%s" % i.badge.slug),
            "verify": {
                "type": "hosted",
                "url": request.build_absolute_uri()
                },
            "issuedOn": time.mktime(i.issuedOn.timetuple()),
            "evidence": i.evidence,
            }
        return json_response(data)


def revocation(request):
    r = Revocation.objects.all()
    data = dict(((i.instance.id, i.reason) for i in r))
    return json_response(data)


def claim(request, id=None):
    """ Claim processing """
    i = get_object_or_404(Claim, id=id)
    # THIS IS UGLY - FIX!
    if i.recipient:
        i.multiple = False
    if request.method == "POST":
        if i.code:
            if i.code == request.POST["code"]:
                i.recipient = request.POST["recipient"]
        else:
            i.recipient = request.POST["recipient"]
    if not i.instance and i.recipient:
        i.instance = create_new_instance(i.badge, i.recipient, i.evidence)
    if not i.multiple:
        i.save()
    data = {"claim": i, }
    if i.instance:
        data["assertion"] = request.build_absolute_uri(
            "../badge/%s/instance/%s" % (
                i.badge.slug,
                i.instance.id
                ))
    data.update(csrf(request))
    return render_to_response("claim.html", data)


def home(request):
    data = {"badges": Badge.objects.all()[0:20], }
    return render_to_response("start.html", data)


def issue_api(request):
    required_parameters = [
        'id', 'badge', 'recipient', 'signature'
        ]
    gd = request.GET
    data = {}
    if not reduce(lambda x, y: x and y,
                  map(lambda x: x in gd.keys(), required_parameters)):
        data = {
            "status": "error",
            "reason":
            "not all required parameters: %s " % required_parameters
            }
        return json_response(data)
    try:
        app = Application.objects.get(id=gd['id'])
    except ObjectDoesNotExist:
        data = {"status": "error",
                "reason": "invalid application credentials"}
        return json_response(data)
    try:
        b = Badge.objects.get(slug=gd['badge'])
    except ObjectDoesNotExist:
        data = {"status": "error",
                "reason": "badge %s does not exist" % gd['badge'], }
        return json_response(data)
    try:
        app.badges.get(id=b.id)
    except ObjectDoesNotExist:
        data = {
            "status": "error",
            "reason":
            "the application is not allowed to issue badge %s" % b.slug,
            }
        return json_response(data)
    if not gd['signature'] == hashlib.sha256(gd['badge'] +
                                             gd['recipient'] +
                                             app.key).hexdigest():
        data = {"status": "error",
                "reason": "invalid signature"}
        return json_response(data)
    c = create_or_return_claim(b, gd['recipient'],
                               gd.get('evidence', None))
    data = {"status": "success",
            "claim": request.build_absolute_uri("../claim/%s" % c.id),
            "assertion": request.build_absolute_uri(
                "../badge/%s/instance/%s" % (b.slug,
                                             c.instance.id)),
            "badge": {
                "name": b.name,
                "slug": b.slug,
                "image": b.image,
                "description": b.description,
                "criteria": b.criteria,
                },
            }
    return json_response(data)


def stats(request):
    cur=connection.cursor()
    cur.execute("""select count(id), badge_id from 
                okbadger_instance group by badge_id""");
    bd=cur.fetchall()
    data=[]
    for b in bd:
        badge=Badge.objects.get(id=b[1])
        data.append({
                    "name": badge.name,
                    "id": badge.id,
                    "image": badge.image,
                    "count": b[0]
                    })
    return render_to_response("stats.html",{"badges": json.dumps(data)})
