from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AdicionarUsuarioForm
from .models import CustomUser, Vacancia


class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Vacancia)
class VacanciaAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(CustomUser, CustomUserAdmin)
