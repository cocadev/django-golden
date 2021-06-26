from django.db import models
from django.contrib.auth.models import (AbstractBaseUser)
from django.core.validators import RegexValidator
from django.urls import reverse
from authentication.models import Client
from .utils import Units


class Employee(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=255,
                                  verbose_name='First name',
                                  blank=True)

    last_name = models.CharField(max_length=255,
                                 verbose_name='Last name',
                                 blank=True)

    phone_number = models.CharField(validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                                               message="Phone number must be entered in the format: "
                                                                       "'+49172578420'. Up to 15 digits allowed.")],
                                    max_length=17,
                                    verbose_name='Phone number',
                                    blank=True)

    business_address_street = models.CharField(max_length=254,
                                               verbose_name='Street',
                                               blank=True)

    business_address_house_number = models.CharField(max_length=5,
                                                     verbose_name='House number',
                                                     blank=True)

    business_address_zipecode = models.CharField(max_length=5,
                                                 verbose_name='Zip code',
                                                 blank=True)

    business_address_city = models.CharField(max_length=5,
                                             verbose_name='City',
                                             choices=(
                                                 ('A', 'Aachen'),
                                                 ('HH', 'Hamburg'),
                                                 ('H', 'Hannover')
                                             ),
                                             blank=True)

    business_address_country = models.CharField(max_length=3,
                                                verbose_name='Country',
                                                choices=(
                                                    ('DE', 'Germany'),
                                                ),
                                                blank=True)
    position = models.CharField(max_length=255,
                                verbose_name='Position',
                                blank=True)

    note = models.TextField(verbose_name='Note',
                            blank=True)

    birthday = models.DateTimeField(
        verbose_name='Creation date',
        null=True,
        blank=True
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
        blank=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return False

    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return False

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return False


class Category(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Name',
                            blank=True)
    is_active = models.BooleanField(default=True)

    description = models.TextField(verbose_name='Description',
                                   blank=True)

    image = models.ImageField(null=True, blank=True, upload_to="categories/")

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
        blank=True
    )

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    @property
    def absolute_url(self):
        return reverse('secure.category.profile', args=[str(self.id)])

    @property
    def product_absolute_url(self):
        return reverse('secure.category.products', args=[str(self.id)])

    @property
    def get_products(self):
        return self.product_set.filter(is_active=True).all()

    @property
    def get_products_count(self):
        return self.product_set.filter(is_active=True).count()


class Product(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Name',
                            blank=True)
    article_number = models.CharField(max_length=255,
                                      verbose_name='Article number',
                                      blank=True)

    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    units = models.CharField(max_length=50,
                             verbose_name='Units',
                             choices=Units.choices,
                             blank=True)

    offer_start = models.DateTimeField(
        verbose_name='End offer',
        null=True,
        blank=True
    )

    offer_end = models.DateTimeField(
        verbose_name='Start offer',
        null=True,
        blank=True
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
        blank=True
    )

    is_active = models.BooleanField(default=True)

    short_description = models.TextField(max_length=120, verbose_name='Short description',
                                         blank=True)

    description = models.TextField(verbose_name='Note',
                                   blank=True)

    image = models.ImageField(null=True, blank=True, upload_to="products/")

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def get_price(self):
        if self.price:
            return str(self.price) + " €"
        return ""

    def active_units(selfs):
        return selfs.priceunit_set.filter(is_active=True)

    def get_allowed_units(selfs):
        return selfs._meta.get_field('units').choices


class PriceUnit(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Unit Name',
                            choices=Units.choices,
                            blank=True)

    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
        blank=True
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def get_price(self):
        if self.price:
            return str(self.price) + " €"
        return ""

    @property
    def get_price_unit(self):
        if self.price:
            return str(self.price) + " €/" + self.get_name_display()
        return self.get_name_display()


class Settings(models.Model):
    company_name = models.CharField(max_length=255,
                                    verbose_name='Name',
                                    blank=True)

    company_email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    company_phone_number = models.CharField(validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                                                       message="Phone number must be entered in the format: "
                                                                               "'+49172578420'. Up to 15 digits allowed.")],
                                            max_length=17,
                                            verbose_name='Phone number',
                                            blank=True)

    company_fax_number = models.CharField(validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                                                     message="Phone number must be entered in the format: "
                                                                             "'+49172578420'. Up to 15 digits allowed.")],
                                          max_length=17,
                                          verbose_name='Phone number',
                                          blank=True)

    company_address_street = models.CharField(max_length=254,
                                              verbose_name='Street',
                                              blank=True)

    company_address_house_number = models.CharField(max_length=5,
                                                    verbose_name='House number',
                                                    blank=True)

    company_address_zipecode = models.CharField(max_length=5,
                                                verbose_name='Zip code',
                                                blank=True)

    company_address_city = models.CharField(max_length=5,
                                            verbose_name='City',
                                            choices=(
                                                ('A', 'Aachen'),
                                                ('HH', 'Hamburg'),
                                                ('H', 'Hannover')
                                            ),
                                            blank=True)

    company_address_country = models.CharField(max_length=3,
                                               verbose_name='Country',
                                               choices=(
                                                   ('de', 'Germany'),

                                               ),
                                               default="de",
                                               blank=True)

    image = models.ImageField(null=True, blank=True, upload_to="companies/")

    language = models.CharField(max_length=5,
                                verbose_name='City',
                                choices=(
                                    ('de', 'German'),
                                    ('fr', 'Français'),
                                    ('gb', 'English'),
                                    ('tr', 'Turkish')
                                ),
                                default='de',
                                blank=True)

    tax_number = models.CharField(max_length=255,
                                  verbose_name='Tax number',
                                  blank=True)

    conditions = models.TextField(verbose_name='Terms & Conditions',
                                  blank=True)

    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
        blank=True
    )

    def __str__(self):
        return self.company_name

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url


class Invoice(models.Model):
    uuid = models.CharField(max_length=255,
                            verbose_name='Invoice Number')

    client = models.ForeignKey(Client, on_delete=models.PROTECT)

    created_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Creation date',
        blank=True
    )

    issue_date = models.DateTimeField(
        verbose_name='Issue Date',
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    state = models.IntegerField(default=1, choices=(
        (1, 'received'),
        (2, 'in-progress'),
        (3, 'delivered'),
        (4, 'canceled'),
        (5, 'returned'),
    ))

    def __str__(self):
        return self.uuid

    def get_active_orders(self):
        return self.order_set.filter(is_active=True)


class Order(models.Model):
    order_number = models.CharField(max_length=255,
                                    verbose_name='Order Number')

    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, default=None)

    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    units = models.CharField(max_length=50,
                             verbose_name='Units',
                             choices=Units.choices,
                             blank=True)

    delivery_date = models.DateTimeField(
        verbose_name='Delivery date',
        null=True,
        blank=True
    )

    description = models.TextField(verbose_name='Description',
                                   blank=True)

    is_active = models.BooleanField(default=True)

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
        blank=True
    )

    def __str__(self):
        return self.order_number

    def get_price(self):
        if self.price:
            return str(self.price) + " €"
        return ""
