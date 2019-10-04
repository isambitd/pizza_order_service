from rest_framework import serializers
from .models import Pizza, Customer, Order, Item


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone_number', 'created', 'modified']


class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ['id', 'flavour', 'description', 'created', 'modified']


class ItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Item
        fields = ['id', 'count', 'size', 'pizza', 'created', 'modified']


class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'customer', 'items', 'created', 'modified']

    def create(self, validated_data):
        items = validated_data.pop('items')
        if len(items) == 0:
            raise serializers.ValidationError(
                {"message": "items cannot be empty!"})
        for item in items:
            if "count" in item and item["count"] == 0:
                raise serializers.ValidationError(
                    {"message": "items cannot be with count 0!"})
        if "status" in validated_data:
            validated_data.pop("status")
        order = Order.objects.create(**validated_data)
        for item in items:
            if "id" in item:
                item.pop("id")
            if item.get("count") > 0:
                Item.objects.create(order=order, **item)
        return order

    def update(self, order, validated_data):
        items_to_update = []
        if order.status != 3:
            if "items" in validated_data.keys():
                items_to_update = validated_data.pop('items')
            order.status = validated_data.get("status", order.status)
            if order.customer.id == validated_data["customer"].id:
                order.save()
                for item in items_to_update:
                    if Item.objects.filter(
                            order=order, pizza=item.get("pizza"), size=item.get("size")).exists():
                        i = Item.objects.get(
                            order=order, pizza=item.get("pizza"), size=item.get("size"))
                        i.count = item.get("count", i.count)
                        if i.count == 0:
                            i.delete()
                        else:
                            i.save()
                    elif "id" in item.keys():
                        if Item.objects.filter(id=item["id"]).exists():
                            i = Item.objects.get(id=item["id"])
                            i.count = item.get("count", i.count)
                            i.size = item.get("size", i.size)
                            i.pizza = item.get("pizza", i.pizza)
                            if i.count == 0:
                                i.delete()
                            else:
                                i.save()
                    elif item.get("count") > 0:
                        Item.objects.create(order=order, **item)
        return order
