from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
	fieldsets = (

		(None, {'fields':('email', 'password', 'fname', 'username','uploaded', 'followers','following','bio','profile_pic', 'liked_posts', 'notifications', 'last_login')}),
		('Permissions', {'fields':(
			'is_active',
			'is_staff',
			'is_superuser',
			'groups',
			'user_permissions',
		)}),
	)

	add_fieldsets = (
		(
			None,
			{
				'classes':('wide',),
				'fields':('email', 'password1', 'password2')
			}
		),	
	)

	list_display = ('email', 'fname', 'username', 'profile_pic', 'uploaded', 'followers', 'following', 'bio', 'liked_posts', 'notifications', 'last_login')
	list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
	seach_fields = ('email',)
	filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)