from django.contrib import admin
from django.contrib.auth.models import User
from .models import Snippet, UserSoftDelete


class SnippetAdmin(admin.ModelAdmin):
    readonly_fields = ("highlighted",)


class UserSoftDeleteInline(admin.TabularInline):
    model = UserSoftDelete
    can_delete = False
    verbose_name = "Soft Delete Status"
    fields = ["is_deleted"]


class MyAdminView(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.soft_delete_status:
            obj.soft_delete_status.save()


class CustomUserAdmin(admin.ModelAdmin):
    inlines = [
        UserSoftDeleteInline,
    ]


admin.site.register(Snippet, SnippetAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
