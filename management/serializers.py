from rest_framework import routers, serializers, viewsets
from .models import Employee, Product, Invoice, Order
from authentication.models import Client


class EmployeeSerializer(serializers.ModelSerializer):
    DT_RowId = serializers.SerializerMethodField('get_row_id')

    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'position', 'is_active', 'DT_RowId', 'pk')
        ordering = ('first_name', 'last_name', 'email', 'phone_number', 'position')

    def get_row_id(self, obj):
        return "row_" + str(obj.pk)


class ProductSerializer(serializers.ModelSerializer):
    DT_RowId = serializers.SerializerMethodField('get_row_id')

    class Meta:
        model = Product
        fields = ('image',
                  'name', 'category', 'short_description', 'article_number', 'is_active', 'offer_start', 'offer_end',
                  'DT_RowId',
                  'pk')
        ordering = ('pk', 'name', 'short_description', 'category', 'article_number', 'offer_start', 'is_active')

    def get_row_id(self, obj):
        return "row_" + str(obj.pk)

    def to_representation(self, instance):
        representation = super(ProductSerializer, self).to_representation(instance)
        representation['offer_start'] = instance.offer_start.strftime("%d/%m/%Y") if instance.offer_start else None
        representation['offer_end'] = instance.offer_end.strftime("%d/%m/%Y") if instance.offer_start else None
        representation['period'] = str(representation['offer_start']) + " - " + str(
            representation['offer_end']) if instance.offer_start else None
        representation['category'] = instance.category.name
        return representation


class OrderSerializer(serializers.ModelSerializer):
    DT_RowId = serializers.SerializerMethodField('get_row_id')

    class Meta:
        model = Order
        fields = ('DT_RowId', 'pk', 'order_number', 'product', 'amount', 'delivery_date', 'is_active')

    def get_row_id(self, obj):
        return "row_" + str(obj.pk)


class ClientSerializer(serializers.ModelSerializer):
    DT_RowId = serializers.SerializerMethodField('get_row_id')

    class Meta:
        model = Client
        fields = (
            'DT_RowId', 'pk', 'first_name', 'last_name', 'company_name', 'phone_number', 'tax_number', 'email',
            'business_address_street', 'business_address_house_number', 'business_address_zipecode',
            'get_business_address_city_display', 'get_business_address_country_display', 'is_active')

    def get_row_id(self, obj):
        return "row_" + str(obj.pk)


class InvoicesSerializer(serializers.ModelSerializer):
    DT_RowId = serializers.SerializerMethodField('get_row_id')
    orders = OrderSerializer(source='get_active_orders', many=True)
    client = ClientSerializer(many=False)

    class Meta:
        model = Invoice
        fields = ('uuid', 'is_active', 'DT_RowId', 'pk', 'state', 'orders', 'client', 'issue_date', 'created_date')
        ordering = ('uuid', 'uuid', 'client__first_name', 'uuid', 'state', 'issue_date', 'created_date')

    def to_representation(self, instance):
        representation = super(InvoicesSerializer, self).to_representation(instance)
        representation['created_date'] = instance.created_date.strftime("%d/%m/%Y %H:%M")
        representation['issue_date'] = instance.issue_date.strftime("%d/%m/%Y")
        representation['state'] = instance.get_state_display()
        return representation

    def get_row_id(self, obj):
        return "row_" + str(obj.pk)


class InvoicesClientSerializer(serializers.ModelSerializer):
    DT_RowId = serializers.SerializerMethodField('get_row_id')
    client = ClientSerializer(many=False)

    class Meta:
        model = Invoice
        fields = ('client', 'DT_RowId',)
        ordering = ('uuid', 'uuid', 'client__first_name', 'uuid', 'state', 'created_date')

    def to_representation(self, instance):
        representation = super(InvoicesClientSerializer, self).to_representation(instance)

        return representation

    def get_row_id(self, obj):
        return "row_" + str(obj.pk)
