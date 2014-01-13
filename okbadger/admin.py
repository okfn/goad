from django.contrib import admin
from okbadger.models import *

admin.site.register(Issuer)
admin.site.register(Badge)
admin.site.register(Instance)
admin.site.register(Revocation)


class ClaimAdmin(admin.ModelAdmin):
    model = Claim
    list_display = ('badge', 'recipient', 'evidence')
    readonly_fields = ('id', )


class ApplicationAdmin(admin.ModelAdmin):
    model = Application
    readonly_fields = ('id', )


admin.site.register(Claim, ClaimAdmin)
admin.site.register(Application, ApplicationAdmin)
