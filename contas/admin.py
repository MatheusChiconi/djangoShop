from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioCustomizado

class UsuarioCustomizadoAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
    ('Informações Pessoais', {'fields': ('telefone', 'cpf')}),
    ('Endereço Completo', {'fields': ('cep', 'endereco', 'cidade', 'estado')}),
)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'classes': ('wide',),
            'fields': ('telefone', 'cpf'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'is_staff', 'cpf')

admin.site.register(UsuarioCustomizado, UsuarioCustomizadoAdmin)
