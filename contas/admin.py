from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioCustomizado

class UsuarioCustomizadoAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('telefone', 'cpf')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'classes': ('wide',),
            'fields': ('telefone', 'cpf'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'telefone', 'cpf')

admin.site.register(UsuarioCustomizado, UsuarioCustomizadoAdmin)
