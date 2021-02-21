from rest_framework import serializers
from .models import Product, Order, OrderProduct


class ProductListSerializers(serializers.ModelSerializer):

    class Meta:

        model = Product
        exclude = ['description']
        

class ProductDetailSerializers(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:

        model = Product
        fields = ('product_name', 'image_url', 'description', 'price', 'slug')

    def get_image_url(self, obj):
        return obj.image.url

class OrderProductSerializer(serializers.ModelSerializer):

    product = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderProduct
        fields = (
            # 'id',
            'product',
            # 'item_variations',
            'quantity',
            'final_price'

        )

    def get_product(self, obj):
        return ProductListSerializers(obj.Product).data

    def get_final_price(self, obj):
        return obj.get_final_price()


class CartSerializers(serializers.ModelSerializer):

    order_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:

        model = Order
        fields = (
            'id',
            'order_items',
            'total_price'
        )

    def get_order_items(self, obj):
        return OrderProductSerializer(obj.Product.all(), many=True).data

    def get_total_price(self, obj):
        return obj.get_total_price()