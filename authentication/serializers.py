from rest_framework import  serializers
from .models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    DT_RowId = serializers.SerializerMethodField('get_row_id')

    class Meta:
        model = Tenant
        fields = ('DT_RowId', 'domain_url', 'store_id',)
        ordering = ('first_name', 'last_name', 'email', 'phone_number', 'position')

    def get_row_id(self, obj):
        return str(obj.pk)


