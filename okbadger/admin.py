from django.contrib import admin
from okbadger.models import Issuer,Badge,Instance,Revocation

admin.site.register(Issuer)
admin.site.register(Badge)
admin.site.register(Instance)
admin.site.register(Revocation)

# Register your models here.
