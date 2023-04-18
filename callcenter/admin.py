from django.contrib import admin
from callcenter.models import TxRegime, SymptomQuestion, Stage, SocialPlatform, StateRegion, Township, Channel, Organization, SiteLocation, InvestigationType, InvestigationResult

# Register your models here.

admin.site.register(SymptomQuestion)
admin.site.register(Stage)
admin.site.register(SocialPlatform)
admin.site.register(StateRegion)
admin.site.register(Township)
admin.site.register(Channel)
admin.site.register(Organization)
admin.site.register(SiteLocation)
admin.site.register(InvestigationType)
admin.site.register(InvestigationResult)
admin.site.register(TxRegime)
