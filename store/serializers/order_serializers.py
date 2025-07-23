from rest_framework import serializers
from ..models import Order, OrderItem, Animal

class CreateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('animal',)

class CreateOrderSerializer(serializers.ModelSerializer):
    items = CreateOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('items',)

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
        
class OrderItemSerializer(serializers.ModelSerializer):
    animal = serializers.StringRelatedField()
    class Meta:
        model = OrderItem
        fields = ('id', 'animal', 'price')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    buyer = serializers.StringRelatedField()
    
    class Meta:
        model = Order
        fields = ('id', 'buyer', 'status', 'total_price', 'created_at', 'items')