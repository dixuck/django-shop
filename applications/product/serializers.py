from rest_framework import serializers

from .models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ['product']


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'slug': {'read_only': True},
        }


    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user'] = user
        images = validated_data.pop('image', None)
        product = Product.objects.create(**validated_data)
        if images is not None:
            imgs = [ProductImage(product=product, image=image) for image in images]
            ProductImage.objects.bulk_create(imgs)
        return product

    def to_representation(self, instance):
        represenation = super().to_representation(instance)
        represenation['images'] = ProductImageSerializer(instance.images.all(), many=True).data
        return represenation
 