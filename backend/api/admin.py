from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import FieldDoesNotExist

from api import models
from api import forms as opt_forms
from api.models import MyUser


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class MyUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'is_admin',)
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    ordering = ('name',)

    def to_field_allowed(self, request, to_field):
        """see: https://www.lasolution.be/blog/related-manytomanyfield-django-admin-site-continued.html"""
        rv = super(ClientAdmin, self).to_field_allowed(request, to_field)
        if not rv:
            opts = self.model._meta
            try:
                return opts.get_field(to_field) == opts.pk and len(opts.many_to_many)
            except FieldDoesNotExist:
                return False
        return rv


class EmployeeAdmin(admin.ModelAdmin):
    form = opt_forms.CompanyForm

    list_display = ('id', 'user', 'is_technician', '_client')
    ordering = ('user',)
    fieldsets = (
        (None, {'fields': ('user', 'is_technician', 'clients')}),
    )

    def _client(self, instance):
        return ",".join([company.name for company in instance.clients.all()])


class DaemonAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip', 'subnet', 'gateway', 'vlan', 'hostname',)
    ordering = ('client',)


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.Employee, EmployeeAdmin)
admin.site.register(models.Daemon, DaemonAdmin)
