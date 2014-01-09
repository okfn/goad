from okbadger.models import Instance
from django.core.exceptions import ObjectDoesNotExist

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
