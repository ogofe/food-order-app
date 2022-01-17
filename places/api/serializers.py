from rest_framework.serializers import (
	ModelSerializer,
	StringRelatedField,
	HyperlinkedRelatedField,
)


from ..models import *



class UserSerializer(ModelSerializer):
	class Meta:
		fields = ('first_name', 'last_name', 'email', 'token')
		model = User



class CustomerSerializer(ModelSerializer):
	user = UserSerializer()
	class Meta:
		fields = '__all__'
		model = Customer


class FoodImageSerializer(ModelSerializer):
	class Meta:
		fields =('image',)
		model = FoodImage


class CustomizationOptionSerializer(ModelSerializer):
	class Meta:
		fields = ('option', 'price')
		model = CustomizationOption


class CustomizationSerializer(ModelSerializer):
	options = CustomizationOptionSerializer(many=True)
	class Meta:
		fields = ('title', 'options')
		model = Customization


class FoodSerializer(ModelSerializer):
	# image = FoodImageSerializer()
	images = FoodImageSerializer(many=True)
	customizations = CustomizationSerializer(many=True)
	class Meta:
		fields = ('id', 'title', 'subtitle', 'about', 'price', 'image', 'images', 'category', 'customizations')
		model = FoodItem


class OrderItemSerializer(ModelSerializer):
	class Meta:
		fields = '__all__'
		model = OrderItem


class OrderSerializer(ModelSerializer):
	class Meta:
		fields = '__all__'
		model = Order
