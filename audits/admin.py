from django.contrib import admin
from audits.models import AuditLog


class AuditLogsAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "model_name", "model_id", "action", "action_taken_on")


admin.site.register(AuditLog, AuditLogsAdmin)
