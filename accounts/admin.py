from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Account, UserProfile, Engineer, Supervisor, StoreKeeper, Supplier, Finance, Driver, ShipmentManager

@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'address', 'city', 'county', 'date_joined', 'last_login', 'is_staff', 'status', 'is_vendor')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    list_display_links = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    list_editable = ['status']
    filter_horizontal = ()
    list_filter = ['status', 'email', 'is_vendor']

@admin.register(Engineer)
class EngineerAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'address', 'city', 'county', 'date_joined', 'last_login', 'is_staff', 'status']
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    list_display_links = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    list_editable = ['status']
    filter_horizontal = ()
    list_filter = ['status', 'email', 'is_vendor']

@admin.register(ShipmentManager)
class ShipmentManagerAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'address', 'city', 'county', 'date_joined', 'last_login', 'is_staff', 'status']
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    list_display_links = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    list_editable = ['status']
    filter_horizontal = ()
    list_filter = ['status', 'email', 'is_vendor']
    
@admin.register(Supervisor)
class EngineerAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'address', 'city', 'county', 'date_joined', 'last_login', 'is_staff', 'status']
    ssearch_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    list_display_links = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    list_editable = ['status']
    filter_horizontal = ()
    list_filter = ['status', 'email', 'is_vendor']

    
@admin.register(StoreKeeper)
class StorekeeperAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'address', 'city', 'county', 'date_joined', 'last_login', 'is_staff', 'status']
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    list_display_links = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    list_editable = ['status']
    filter_horizontal = ()
    list_filter = ['status', 'email', 'is_vendor']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'address', 'city', 'county', 'date_joined', 'last_login', 'is_staff', 'status']
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    list_display_links = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    list_editable = ['status']
    filter_horizontal = ()
    list_filter = ['status', 'email', 'is_vendor']


@admin.register(Finance)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'address', 'city', 'county', 'date_joined', 'last_login', 'is_staff', 'status']
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    list_display_links = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    list_editable = ['status']
    filter_horizontal = ()
    list_filter = ['status', 'email', 'is_vendor']


@admin.register(Driver)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'address', 'city', 'county', 'date_joined', 'last_login', 'is_staff', 'status']
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    list_display_links = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    list_editable = ['status']
    filter_horizontal = ()
    list_filter = ['status', 'email', 'is_vendor']



@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # display user profile image thumbnail in admin
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.profile_picture.url))


    list_display = ('thumbnail', 'user', 'city', 'county',  'address_line_1', 'address_line_2')
    search_fields = ('user__email', 'user__username', 'user__first_name', 'user__last_name', 'phone_number')
    list_display_links = ('user',)
    ordering = ('-user',)

    
    filter_horizontal = ()
    list_filter = ('city', 'county')
    fieldsets = ()

