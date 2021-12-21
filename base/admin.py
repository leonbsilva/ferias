from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AdicionarUsuarioForm
from .models import CustomUser, Vacancia


class CustomUserAdmin(UserAdmin):
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Vacancia)
class VacanciaAdmin(admin.ModelAdmin):
    list_display = ['servidor', 'situacao', 'data_solicitacao', 'ano_base', 'data_inicio', 'data_fim',
                    'data_avaliacao', 'observacao']
    search_fields = ['servidor__username']

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(CustomUser, CustomUserAdmin)
