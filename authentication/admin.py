from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from authentication.models import User, Dealer, Tenant, Client


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class DealerCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Dealer
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class DealerChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Dealer
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    actions = ['delete_selected']
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'is_admin', 'is_active')
    list_filter = ('date_joined', 'business_address_city', 'is_active', 'is_admin')
    fieldsets = (
        ('Login data', {'classes': ('wide', 'extrapretty'), 'fields': ('email', 'password')}),
        ('Personal info', {'classes': ('wide', 'extrapretty'), 'fields': ('first_name', 'last_name',)}),
        ('Business address', {'classes': ('wide', 'extrapretty'), 'fields': ('business_address_street',
                                                                             'business_address_house_number',
                                                                             'business_address_zipecode',
                                                                             'business_address_country',
                                                                             'business_address_city')}),
        ('Permission info', {'fields': ('is_active', 'is_admin')})
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ('Login data', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Business address', {'fields': ('business_address_street',
                                         'business_address_house_number',
                                         'business_address_zipecode',
                                         'business_address_country',
                                         'business_address_city')}),
        ('Permission info', {'fields': ('is_active', 'is_admin')}),
    )

    search_fields = ('email',)
    ordering = ('date_joined',)
    filter_horizontal = ()

    def get_actions(self, request):
        # Disable delete
        actions = super(UserAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class DealerAdmin(BaseUserAdmin):
    form = DealerChangeForm
    add_form = DealerCreationForm

    actions = ['publish_selected', 'hide_selected', 'delete_selected']
    list_filter = ('email', 'tenant')
    search_fields = ('email',)
    list_display = ('email', 'tenant', 'first_name', 'last_name', 'date_joined', 'is_active')
    ordering = ('date_joined', 'tenant')
    filter_horizontal = ()
    # overrides get_fieldsets to use this attribute when creating a user.
    fieldsets = (
        ('Login data', {'classes': ('wide', 'extrapretty'), 'fields': ('email', 'password')}),
        ('Personal info', {'classes': ('wide', 'extrapretty'), 'fields': ('first_name', 'last_name',)}),
        ('Business address', {'fields': ('business_address_street',
                                         'business_address_house_number',
                                         'business_address_zipecode',
                                         'business_address_country',
                                         'business_address_city')}),
        ('Permission info', {'fields': ('is_active',)})
    )
    add_fieldsets = (
        ('Login data', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'tenant')}
         ),
        ('Personal info', {'classes': ('wide', 'extrapretty'), 'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Business address', {'classes': ('wide', 'extrapretty'), 'fields': ('business_address_street',
                                                                             'business_address_house_number',
                                                                             'business_address_zipecode',
                                                                             'business_address_country',
                                                                             'business_address_city')}),
        ('Permission info', {'fields': ('is_active',)}),
    )

    def get_actions(self, request):
        # Disable delete
        actions = super(DealerAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

        # Now register the new UserAdmin...


class ClientAdmin(BaseUserAdmin):
    form = DealerChangeForm
    add_form = DealerCreationForm

    actions = ['publish_selected', 'hide_selected', 'delete_selected']
    list_filter = ('email',)
    search_fields = ('email',)
    list_display = ('company_name', 'email', 'first_name', 'last_name', 'date_joined', 'is_active')
    ordering = ('date_joined',)
    filter_horizontal = ()
    # overrides get_fieldsets to use this attribute when creating a user.
    fieldsets = (
        ('Login data', {'classes': ('wide', 'extrapretty'), 'fields': ('email', 'password')}),
        ('Personal info',
         {'classes': ('wide', 'extrapretty'), 'fields': ('first_name', 'last_name', ('phone_number', 'fax_number'))}),
        ('Business address', {'fields': ('business_address_street',
                                         'business_address_house_number',
                                         'business_address_zipecode',
                                         'business_address_country',
                                         'business_address_city')}),
        ('Permission info', {'fields': ('is_active',)})
    )
    add_fieldsets = (
        ('Login data', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
        ('Personal info', {'classes': ('wide', 'extrapretty'),
                           'fields': (('first_name', 'last_name'), ('company_name', 'tax_number'),
                                      ('phone_number', 'fax_number'))}),
        ('Business address', {'classes': ('wide', 'extrapretty'), 'fields': ('business_address_street',
                                                                             'business_address_house_number',
                                                                             'business_address_zipecode',
                                                                             'business_address_country',
                                                                             'business_address_city')}),
        ('Permission info', {'fields': ('is_active',)}),
    )

    def get_actions(self, request):
        # Disable delete
        actions = super(ClientAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

        # Now register the new UserAdmin...


class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain_url', 'schema_name', 'store_id', 'date_joined', 'is_active')
    list_filter = ('domain_url', 'date_joined', 'store_id', 'is_active')
    search_fields = ('domain_url', 'store_id',)
    ordering = ('name',)
    filter_horizontal = ()

    # overrides get_fieldsets to use this attribute when creating a user.
    fieldsets = (
        ('Personal info',
         {'classes': ('wide', 'extrapretty'), 'fields': ('name', 'domain_url', 'schema_name', 'store_id')}),

        ('Permission info', {'fields': ('is_active',)}),
    )

    def get_actions(self, request):
        # Disable delete
        actions = super(TenantAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(Dealer, DealerAdmin)
admin.site.register(Tenant, TenantAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.unregister(Group)
