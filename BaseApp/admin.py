from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from . import models
from django.utils.translation import gettext_lazy as _


# Register your models here.
@register(models.Teacher)
class TeacherAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("gender", "email", "phone")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_class_tr",
                    "is_superuser",
                    "is_teacher",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", 'email', "password1", "password2"),
            },
        ),
    )
    list_display = ['username', 'gender', 'email', 'phone', 'is_class_tr']


class RecordInline(admin.TabularInline):
    model = models.ClassRecord


@register(models.ClassCaptain)
class ClassCaptain(admin.ModelAdmin):
    list_display = ('username', 'gender', 'status')
    inlines = [RecordInline]


admin.site.register(models.Subject)
admin.site.register(models.ClassRoom)
admin.site.register(models.Topic)
admin.site.register(models.ClassRecord)
