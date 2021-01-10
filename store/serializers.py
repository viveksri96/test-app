from rest_framework import serializers
from store.models import Store, Product, Category
from accounts.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", 'name']

    def create(self, validated_data):
        return Category.objects.get_or_create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number']
        read_only_fields = ['id']

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class StoreSerializer(serializers.ModelSerializer):
    # owner = UserSerializer(read_only=True)

    class Meta:
        model = Store
        fields = [
            "id",
            # "owner",
            "name",
            "address"
        ]

    def create(self, validated_data):
        validated_data["owner"] = self.context["user"]
        store = Store.objects.create(**validated_data)
        return store


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'mrp',
            'sale_price',
            'image',
            'category',
            'store',
        ]
