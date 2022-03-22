from rest_framework.serializers import (
	ModelSerializer,
	StringRelatedField,
	HyperlinkedRelatedField,
)


from ..models import *

class PermissionSerializer(ModelSerializer):
	class Meta:
		model = Permission
		fields = '__all__'


class UserSerializer(ModelSerializer):

	class Meta:
		fields = ('first_name', 'last_name', 'email', 'username')
		model = User


class StaffSerializer(ModelSerializer):
	user = UserSerializer()
	class Meta:
		fields = ('id', 'user', 'staff_id', 'permissions')
		model = Staff



class CategorySerializer(ModelSerializer):
	class Meta:
		model = Category
		fields = ('id', 'name')


class TagSerializer(ModelSerializer):
	class Meta:
		model = Tag
		fields = ('id', 'tag')


class CustomerSerializer(ModelSerializer):
	user = UserSerializer()
	class Meta:
		fields = '__all__'
		model = Customer


class FoodImageSerializer(ModelSerializer):
	class Meta:
		fields =('image_url',)
		model = FoodImage


class CustomizationOptionSerializer(ModelSerializer):
	class Meta:
		fields = ('option', 'price')
		model = CustomizationOption


class CustomizationSerializer(ModelSerializer):
	options = CustomizationOptionSerializer(many=True)
	default_option = CustomizationOptionSerializer()
	class Meta:
		fields = ('id', 'title', 'options', 'required', 'default_option')
		model = Customization


class FoodSerializer(ModelSerializer):
	images = FoodImageSerializer(many=True)
	customizations = CustomizationSerializer(many=True)
	class Meta:
		fields = ('id', 'title', 'subtitle', 'about',
		 'price', 'image', 'tags', 'images', 
		 'category', 'customizations', 'rating')
		model = FoodItem


class OrderItemSerializer(ModelSerializer):
	item = FoodSerializer()

	class Meta:
		fields = ('item', 'id', 'qty', 'total')
		model = OrderItem


class OrderSerializer(ModelSerializer):
	items = OrderItemSerializer(many=True)
	owner = CustomerSerializer()

	class Meta:
		fields = ('id', 'invoice', 'created_on', 'items', 'owner', 'status', 'delivery_is_on', 'subtotal')
		model = Order


class ReviewSerializer(ModelSerializer):
	food = StringRelatedField()
	reviewer = StringRelatedField()
	class Meta:
		model = Review
		fields = ('id', 'reviewer', 'food', 'rating', 'comment')


class NotificationSerializer(ModelSerializer):
	class Meta:
		model = Notification
		fields = ('id', 'type', 'text')

