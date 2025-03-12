from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ('email',)  # Ordena por email 
    list_display = ('email', 'first_name', 'last_name', 'phone', 'documento', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'documento')
    
    # Configuración de fieldsets para editar usuarios
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'documento')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Configuración para agregar un nuevo usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'documento', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
