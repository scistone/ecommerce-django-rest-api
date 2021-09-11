from rest_framework import serializers
from users.models import CustomerAddress

class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = [
            'first_name',
            'last_name',
            'phone',
            'address',
            'zip_code',
            'city',
            'district',
            'country',
            'address_type',
        ]