from django.contrib import admin
from okbadger.models import Issuer,Badge,Instance,Revocation,Claim,Application

admin.site.register(Issuer)
admin.site.register(Badge)
admin.site.register(Instance)
admin.site.register(Application)
admin.site.register(Revocation)

class ClaimAdmin(admin.ModelAdmin):
  model = Claim
  list_display = ('badge', 'recipient', 'evidence')
  readonly_fields = ('id',)

admin.site.register(Claim, ClaimAdmin)
