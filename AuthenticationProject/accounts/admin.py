from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from .models import CustomUser, Profile


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'username', 'date_joined', 'is_staff', 'is_active')
    list_filter = ('is_active', 'is_archive', 'date_joined', 'updated')
    search_fields = ('first_name', 'last_name', 'email',)
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True, is_archive=False)
        self.message_user(request, ngettext(
            '%d User was successfully marked as active.',
            '%d Users were successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    make_active.short_description = "Mark selected users as active"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False, is_archive=True)
        self.message_user(request, ngettext(
            '%d User was successfully marked as inactive.',
            '%d Users were successfully marked as inactive.',
            updated,
        ) % updated, messages.INFO)

    make_inactive.short_description = "Mark selected users as inactive"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
