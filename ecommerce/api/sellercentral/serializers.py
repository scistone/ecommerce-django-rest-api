from rest_framework import serializers
from core.models import Menu,MenuElement

class CreateMenuElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuElement
        fields = [
            "title",
            "category",
            "priority",
            "parent",
        ]
    

class CreateMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            "title",
            "category",
            "menu_type",
            "priority",
        ]