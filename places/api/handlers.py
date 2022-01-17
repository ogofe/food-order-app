import os
from rest_framework.views import APIView
from rest_framework.generics import (
	CreateAPIView,
	ListAPIView,
	RetrieveUpdateDestroyAPIView,
	DestroyAPIView,
)
from django.db.models import Q
from rest_framework.response import Response
from .serializers import (
	FoodSerializer,
	CustomerSerializer,
)
from ..models import *
from rest_framework.decorators import api_view



class IndexView(APIView):
	def get(self, request):
		data = {
			'routing': [
				{
					'endpoint': '/api/',
					'description': 'Display the API index page (this)'
				}
			]
		}
		return Response(data=data)


class CreateFoodItemView(CreateAPIView):
	serializer_class = FoodSerializer

	def post(self, request, **kwargs):
		food_item = FoodItem(
				title=request.data['title'],
				subtitle=request.data['subtitle'],
				price=request.data['price'],
				category=request.data['category'],
				tags=request.data['tags'],
				about=request.data['about']
			)
		food_item.save()
		for image in request.FILES.getlist('image'):
			food_image = FoodImage.objects.create(image)
			food_item.images.add(food_image)
		food_item.save()
		return Response(self.serializer_class(food_item).data)



class EditFoodItemView(RetrieveUpdateDestroyAPIView):
	queryset = FoodItem.objects.all()
	serializer_class = FoodSerializer
	lookup_field = 'pk'

	def post(self, request, **kwargs):
		return Response()



class ListFoodItemView(ListAPIView):
	queryset = FoodItem.objects.all()
	serializer_class = FoodSerializer



class CreateOrderItemView(CreateAPIView):
	serializer_class = FoodSerializer

	def post(self, request, **kwargs):
		food_item = FoodItem(
				title=request.data['title'],
				subtitle=request.data['subtitle'],
				price=request.data['price'],
				category=request.data['category'],
				tags=request.data['tags'],
				about=request.data['about']
			)
		food_item.save()
		for image in request.FILES.getlist('image'):
			food_image = FoodImage.objects.create(image)
			food_item.images.add(food_image)
		food_item.save()
		return Response(self.serializer_class(food_item).data)



class EditOrderItemView(RetrieveUpdateDestroyAPIView):
	queryset = FoodItem.objects.all()
	serializer_class = FoodSerializer
	lookup_field = 'pk'

	def post(self, request, **kwargs):
		return Response()



class ListOrderItemView(ListAPIView):
	queryset = FoodItem.objects.all()
	serializer_class = FoodSerializer



class CreateOrderView(CreateAPIView):
	serializer_class = FoodSerializer

	def post(self, request, **kwargs):
		food_item = FoodItem(
				title=request.data['title'],
				subtitle=request.data['subtitle'],
				price=request.data['price'],
				category=request.data['category'],
				tags=request.data['tags'],
				about=request.data['about']
			)
		food_item.save()
		for image in request.FILES.getlist('image'):
			food_image = FoodImage.objects.create(image)
			food_item.images.add(food_image)
		food_item.save()
		return Response(self.serializer_class(food_item).data)



class EditOrderView(RetrieveUpdateDestroyAPIView):
	queryset = FoodItem.objects.all()
	serializer_class = FoodSerializer
	lookup_field = 'pk'

	def post(self, request, **kwargs):
		return Response()



class ListOrderView(ListAPIView):
	queryset = FoodItem.objects.all()
	serializer_class = FoodSerializer



#----------- Customer Handlers ------------

class SignupView(APIView):
	serializer_class = CustomerSerializer

	def post(self, request):
		user = User(
			email=request.data['email'],
			first_name=request.data['first_name'],
			last_name=request.data['last_name'],
		)
		user.set_password(request.data['password'])
		user.save()
		person = Customer.objects.create(user=user)
		return Response(self.serializer_class(person).data)



class LoginView(APIView):
	serializer_class = CustomerSerializer

	def post(self, request):
		user = User.objects.get(email=request.data['email'])
		if user.check_password(request.data['password']):
			try:
				person = Customer.objects.get(user=user)
				return Response(self.serializer_class(person).data)
			except Customer.DoesNotExist as e:
				return Response(data={'error': True, 'error_text': 'Customer with that email not found!'}, status=404)
		return Response(data={'error': True, 'error_text': 'Customer with that email not found!'}, status=404)



class FoodListView(ListAPIView):
	serializer_class = FoodSerializer
	queryset = FoodItem.objects.all()

	def get(self, request):
		qs = self.get_queryset()
		if request.GET.get('search', None):
			search = request.GET.get('search')
			qs = qs.filter(
				Q(title__icontains=search)|
				Q(subtitle__icontains=search)|
				Q(category__icontains=search)
			)
		res = {
			'error': None,
			"items": self.serializer_class(qs, many=True).data
		}
		return Response(data=res, status=200)



# consumer functions
def add_to_cart(data, cart):
	return Response()


def remove_from_cart(data, cart):
	return Response()


def add_to_favorites(request):
	return Response()

@api_view(["POST"])
def remove_from_favorites(request):
	item = None
	return Response()


@api_view(["GET"])
def list_all_food(request):
	qs = FoodItem.objects.all()
	if request.GET.get('search', None):
		search = request.GET.get('search')
		qs = qs.filter(
			Q(title__icontains=search)|
			Q(subtitle__icontains=search)|
			Q(category__icontains=search)
		)
	res = {
		'error': None,
		"items": FoodSerializer(qs, many=True).data
	}
	return Response(data=res, status=200)


@api_view(["GET"])
def item_detail_view(request, **kwargs):
	item = FoodItem.objects.get(id=kwargs['pk'])
	res = {
		'item': FoodSerializer(item).data,
		'error': None
	}
	return Response(status=200, data=res)


@api_view(["GET", "POST"])
def cart_view(request):
	print(request.user)

	if not request.user.is_authenticated:
		raise Exception("....Unauthorized....")
	qs = request.user.customer.orders.all()
	if request.method == "POST":
		if request.data['action'] == 'add-to-cart':
			food_item = FoodItem.objects.get(id=item)
			order_item = OrderItem(
				item=food_item
			)
			item.save()
			if request.data.get('customizations', None):
				for custom in request.data['customizations']:
					customization = Customization.objects.filter(
							food_item=food_item
						).get(
							title=custom['title']
						)
					option = OrderCustomization(
						customization=customization,
						option=customization.options.all().get(
								option=custom['choice']
							)
						)
					order_item.customizations.add(option)
				order_item.save()
		elif request.data['action'] == 'remove-from-cart':
			order_item = OrderItem.objects.get(
					id=request.data['item']
				)
			order_item.delete()
	res = {
		'error': None,
		"items": CartItemSerializer(qs, many=True).data
	}
	return Response(data=res, status=200)


@api_view(["GET", "POST"])
def leave_a_review(request):
	if request.method == "POST":
		review = Review(
			by=request.user.customer,
			rating=request.data['rating'],
			food=FoodItem.objects.get(id=request.data['food_item']),
			comment=request.data['comment']
		)
		review.save()
		return Response()

	# GET : check if a user has reviewed this item
	try:
		review = Review.objects.get(food=FoodItem.objects.get(id=request.GET.get['food_item']))
		if review.comment:
			res = {
				'error': None,
				'user_has_review' : True
			}
		else:
			res = {
				'error': None,
				'user_has_review' : False
			}
	except Review.DoesNotExist:
		res = {
			'error': None,
			'user_has_review' : False

		}
	return Response(status=200, data=res)