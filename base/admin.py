from django.contrib import admin
from django.contrib.admin import display
from django.contrib.auth.admin import UserAdmin

from .forms import AdicionarUsuarioForm, CustomUserChangeForm
from .models import CustomUser, Vacancia


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'matricula', 'first_name', 'last_name', 'data_admissao', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    form = CustomUserChangeForm
    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'matricula', 'data_admissao')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'matricula', 'data_admissao')}),
    )


@admin.register(Vacancia)
class VacanciaAdmin(admin.ModelAdmin):
    list_display = ['servidor', 'situacao', 'data_solicitacao', 'ano_base', 'data_inicio', 'data_fim',
                    'data_avaliacao', 'observacao', 'get_matricula']
    search_fields = ['servidor__username', 'servidor__first_name', 'situacao', 'servidor__matricula']

    @display(ordering='servidor__matricula', description='Matrícula')
    def get_matricula(self, obj):
        return obj.servidor.matricula

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
