from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'  # Esto incluirá todos los campos del modelo
#Validadcion de precio positivo
    def validate_prince(self,value):
        if value < 0:
            raise serializers.ValidationError("El precio debe ser un número positivo.")
        return value
    
    def validate_stock(self,value):
        if value < 0:
            raise serializers.ValidationError("El stock debe ser un número positivo.")
        return value
        