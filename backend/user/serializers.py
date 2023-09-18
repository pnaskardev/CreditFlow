from rest_framework import serializers

from . models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
    
    def validate(self, data):
        # Add your custom validation logic here
        email = data.get('email')
        name = data.get('name')
        annual_income = data.get('annual_income')
        adhaar_id = data.get('adhaar_id')

        if not email:
            raise serializers.ValidationError("User must have an email address")
        if annual_income is None or annual_income < 0:
            raise serializers.ValidationError("Annual income must be a non-negative value")
        if not name:
            raise serializers.ValidationError("User must have a name")
        if not adhaar_id:
            raise serializers.ValidationError("User must have an Aadhar ID")

        return data

    def create(self, validated_data):
        return super().create(validated_data)