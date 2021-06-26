from django import forms
from django.core.validators import RegexValidator
from django.conf import settings

from .models import Employee, Product, Category, Settings


class EmployeeCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,
                               validators=[
                                   RegexValidator(r'^.{6,}$', 'Password must has at least 6 characters.')])
    birthday = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)

    def __init__(self, *args, **kwargs):
        super(EmployeeCreationForm, self).__init__(*args, **kwargs)
        # Making name required
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['password'].required = True
        self.fields['birthday'].required = False

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = Employee.objects.get(email=email)
        except Employee.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('The E-mail address is already in use.')

    def save(self, commit=True):
        user = super(EmployeeCreationForm, self).save(commit=False)
        user.email = self.clean_email()

        if commit:
            user.save()

        return user

    class Meta:
        model = Employee
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'password', 'business_address_street',
                  'business_address_zipecode', 'business_address_city', 'business_address_country',
                  'business_address_house_number', 'note', 'birthday', 'position')


class EmployeeChangeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False,
                               validators=[
                                   RegexValidator(r'^.{6,}$', 'Password must has at least 6 characters.')])
    password2 = forms.CharField(widget=forms.PasswordInput, required=False,
                                validators=[
                                    RegexValidator(r'^.{6,}$', 'Password must has at least 6 characters.')])

    birthday = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)

    def __init__(self, *args, **kwargs):
        super(EmployeeChangeForm, self).__init__(*args, **kwargs)
        # Making name required
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['birthday'].required = False

    def save(self, commit=True):
        user = super(EmployeeChangeForm, self).save(commit=False)
        user.password = self.password
        if commit:
            user.save()

        return user

    def clean_email(self):
        # Get the email
        return self.cleaned_data.get('email')

    class Meta:
        model = Employee
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'password2', 'business_address_street',
                  'business_address_zipecode', 'business_address_city', 'business_address_country',
                  'business_address_house_number', 'note', 'birthday', 'position')


class ProductCreationForm(forms.ModelForm):
    offer_period = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(ProductCreationForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['category'].required = True

    def save(self, commit=True):
        product = super(ProductCreationForm, self).save(commit=False)

        if commit:
            product.save()

        return product

    class Meta:
        model = Product
        fields = ('name', 'category', 'article_number', 'image', 'price', 'offer_start', 'short_description',
                  'offer_end', 'description', 'units', 'is_active')


class ProductChangeForm(forms.ModelForm):
    offer_period = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(ProductChangeForm, self).__init__(*args, **kwargs)
        # Making name required
        self.fields['name'].required = True
        self.fields['category'].required = True

    def save(self, commit=True):
        product = super(ProductChangeForm, self).save(commit=False)
        if commit:
            product.save()

        return product

    class Meta:
        model = Product
        fields = ('name', 'category', 'article_number', 'image', 'price', 'offer_start', 'short_description',
                  'offer_end', 'description', 'units',)


class CategoryCUForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryCUForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True

    def save(self, commit=True):
        category = super(CategoryCUForm, self).save(commit=False)

        if commit:
            category.save()

        return category

    class Meta:
        model = Category
        fields = ('name', 'image', 'description', 'is_active')


class SettingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SettingForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        settings = super(SettingForm, self).save(commit=False)

        if commit:
            settings.save()

        return settings

    class Meta:
        model = Settings
        fields = '__all__'
