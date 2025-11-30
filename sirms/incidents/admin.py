from django.contrib import admin
from .models import (
    CustomUser, Curriculum, Track, Grade, Section, IncidentType,
    LegalReference, IncidentReport, Classification, CounselingSession,
    Notification
)

admin.site.register(CustomUser)
admin.site.register(Curriculum)
admin.site.register(Track)
admin.site.register(Grade)
admin.site.register(Section)
admin.site.register(IncidentType)
admin.site.register(LegalReference)
admin.site.register(IncidentReport)
admin.site.register(Classification)
admin.site.register(CounselingSession)
admin.site.register(Notification)
