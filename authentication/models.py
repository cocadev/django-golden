from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from tenant_schemas.models import TenantMixin


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class DealerManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        dealer = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        dealer.set_password(password)
        dealer.save(using=self._db)
        return dealer

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = False
        user.save(using=self._db)
        return user


class ClientManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        dealer = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        dealer.set_password(password)
        dealer.save(using=self._db)
        return dealer

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = False
        user.save(using=self._db)
        return user


class Tenant(TenantMixin):
    name = models.CharField(max_length=63)

    schema_name = models.SlugField(max_length=63)

    is_active = models.BooleanField(default=True)

    store_id = models.SlugField(max_length=6, unique=True)

    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
        blank=True
    )

    auto_create_schema = True
    REQUIRED_FIELDS = ['name', 'domain_url', 'schema_name', 'store_id']

    def __str__(self):
        return self.domain_url


class User(AbstractBaseUser):
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

    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
        blank=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

    @property
    def has_level2_perm(self):
        "Is the user a member of level2"
        return True


class Dealer(AbstractBaseUser):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, primary_key=True)

    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=255,
                                  verbose_name='First name',
                                  blank=True)

    last_name = models.CharField(max_length=255,
                                 verbose_name='Last name',
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
                                                default="DE",
                                                blank=True)

    phone_number = models.CharField(validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                                               message="Phone number must be entered in the format: "
                                                                       "'+49172578420'. Up to 15 digits allowed.")],
                                    max_length=17,
                                    verbose_name='Phone number',
                                    blank=True)

    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
        blank=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = DealerManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return False

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return False

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def has_level2_perm(self):
        "Is the user a member of staff?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return False


class Client(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='E-mail address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=255,
                                  verbose_name='First name',
                                  blank=True)

    last_name = models.CharField(max_length=255,
                                 verbose_name='Last name',
                                 blank=True)

    company_name = models.CharField(max_length=255,
                                    verbose_name='Company name',
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
                                                default="DE",
                                                blank=True)

    phone_number = models.CharField(validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                                               message="Phone number must be entered in the format: "
                                                                       "'+49172578420'. Up to 15 digits allowed.")],
                                    max_length=17,
                                    verbose_name='Phone number',
                                    blank=True)
    fax_number = models.CharField(validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                                             message="Phone number must be entered in the format: "
                                                                     "'+49172578420'. Up to 15 digits allowed.")],
                                  max_length=17,
                                  verbose_name='Fax number',
                                  blank=True)

    tax_number = models.CharField(max_length=255,
                                  verbose_name='Tax number',
                                  blank=True)

    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
        blank=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = ClientManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return False

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return False

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def has_level2_perm(self):
        "Is the user a member of staff?"
        return False

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return False
