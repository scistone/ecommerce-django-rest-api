from rest_framework import serializers

from order.models import Order,OrderItem

class OrderItemSerializer(serializers.ModelSerializer):    
    class Meta:
        model = OrderItem
        fields = (
            "price",
            "product",
            "quantity",
        )
        extra_kwargs = {'price': {'read_only':True},}

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "city",
            "country",
            "zip_code",
            "phone",
            "items",
            "order_status",
        )
        extra_kwargs = {'order_status': {'read_only':True},}
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
            
        return order