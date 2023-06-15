from rest_framework.serializers import ModelSerializer

from .models import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['slug', 'title']
        read_only_fields = ['slug']