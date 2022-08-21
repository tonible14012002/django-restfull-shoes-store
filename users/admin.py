from django.contrib import admin
from .forms import User, UserChangeForm, UserCreationForm
from django.contrib.auth import  get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

User = get_user_model()


class UserAdmin(DefaultUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'avatar' , 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('email', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        ('Credential', {'fields': ('email', 'password','avatar')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', ('first_name', 'last_name'),
                       ('password1', 'password2'), 
                       ('is_staff', 'is_superuser'),),
        }),
    )
    ordering = ('email',)
    search_fields = ('email',)

admin.site.register(User, UserAdmin)