import os, json
from rest_framework.views import APIView
from rest_framework.generics import (
	CreateAPIView,
	ListAPIView,
	RetrieveUpdateDestroyAPIView,
	DestroyAPIView,
)
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.response import Response
from .serializers import (
	FoodSerializer,
	CustomerSerializer,
	OrderSerializer,
	UserSerializer,
	ReviewSerializer,
	OrderItemSerializer,
	NotificationSerializer,
	CategorySerializer,
	TagSerializer,
)
from django.contrib.auth import login, logout
from ..models import *
from rest_framework.decorators import api_view
from decimal import Decimal


class SignupView(APIView):
	serializer_class = CustomerSerializer

	def post(self, request):
		try:
			user = User(
				username=request.data['phone'],
				email=request.data['email'],
				first_name=request.data['first_name'],
				last_name=request.data['last_name'],
			)
			user.set_password(request.data['password'])
			user.save()
			token = Token(user=user)
			token.save()
			person = Customer(
				user=user, phone=request.data['phone']
			)
			person.save()
			data = {
				'profile': {
					'user': UserSerializer(user).data,
					'token': token.key
				},
				'error': None,
				'response_text': "Successfully created your account"
			}
			return Response(data)
		except Exception as e:
			return Response({'error': True, 'error_text': str(e)})


@api_view(["POST"])
def login_view(request):
	try:
		user = User.objects.get(email=request.data['email'])
		if user.check_password(request.data['password']):
			person = Customer.objects.get(user=user)
			login(request, user)
			data = {
				'user': CustomerSerializer(person).data,
				'token': Token.objects.get_or_create(user=user)[0].key
			}
			return Response(data)
		return Response(data={'error': True, 'error_text': 'User not found!'}, status=404)
	except User.DoesNotExist as e:
		return Response(data={'error': True, 'error_text': 'User not found!'}, status=404)
	except Customer.DoesNotExist as e:
		return Response(data={'error': True, 'error_text': 'User not found!'}, status=404)


def calc_subtotal(items):
	num = 0
	for i in items:
		num += i.total
	return Decimal(num)

def calc_deivery_fee(order):
	return Decimal('7.00')


def calc_vat(order):
	return Decimal('1.23')


def calc_processing_fee(order):
	return Decimal('2.03')


@api_view(["GET"])
def search_view(request):
	query = request.GET.get('query', None)
	_filter = request.GET.get('filter', None)

	if query:
		items = FoodItem.objects.filter(title__icontains=query)
		if _filter:
			items = items.filter(category__name__iexact=_filter)
		paginator = PageNumberPagination()
		paginator.page_size = 20
		page = dict(paginator.get_paginated_response(
				paginator.paginate_queryset(items, request)
			).data)
		results = FoodSerializer(page['results'], many=True).data
		res = {
			'error': None,
			"results": results,
			'next': page['next'],
			'previous': page['previous'],
		}
	else:
		res = {
			'error': True,
			'error_text': "Search param is missing"
		}
	return Response(res)



@api_view(["GET"])
def menu_view(request):
	qs = FoodItem.objects.all().order_by('-id')
	paginator = PageNumberPagination()
	paginator.page_size = 4
	page_size_query_param = 'page_size'
	try:
		page = dict(paginator.get_paginated_response(
				paginator.paginate_queryset(qs, request)
			).data)

		if request.GET.get('search', None):
			search = request.GET.get('search')
			qs = qs.filter(
				Q(title__icontains=search)|
				Q(subtitle__icontains=search)|
				Q(category__icontains=search)
			)
		res = {
			'error': None,
			"menu": FoodSerializer(page['results'], many=True).data,
			'next': page['next'],
			'previous': page['previous'],
			'count': page['count'],
			"categories": CategorySerializer(Category.objects.all(), many=True).data,
			"featured_items": FoodSerializer(FoodItem.objects.filter(featured=True), many=True).data
		}
	except Exception as e:
		
		res = {
			'error': True,
			'error_text': str(e),
		}
		raise e
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
	customer = Customer.objects.get(user=request.user)
	try:
		if request.method == "POST":
			if request.data['action'] == 'add-to-cart':
				food_item = FoodItem.objects.get(id=request.data['item'])
				order_item = OrderItem(item=food_item, qty=request.data.get('qty', 1))
				order_item.save()
				customer.cart.add(order_item)
				customer.save()

				if request.data.get('customizations', None):
					customizations = request.data['customizations']
					for custom in customizations:
						customization = Customization.objects.filter(food=food_item).get(title=custom)
						option = OrderCustomization(
							customization=customization,
							option=customization.options.all().get(
									option=customizations[custom]['option']
								))
						option.save()
						order_item.customizations.add(option)
					order_item.save()
					return Response({'error': None, 'response_text': 'Successfully added item to cart'})

			elif request.data['action'] == 'remove-from-cart':
				order_item = OrderItem.objects.get(
						id=request.data['item']
					)
				order_item.delete()
				return Response({'error': None, 'response_text': 'Successfully removed item from cart'})
		
		qs = customer.cart.all().order_by('-id')
		res = {
			'error': None,
			'subtotal': str(round(calc_subtotal(qs), 2)),
			"items": OrderItemSerializer(qs, many=True).data
		}
		return Response(data=res, status=200)
	except Exception as e:
		return Response(data={'error': True, 'error_text': str(e)}, status=200)


@api_view(["GET", "POST"])
def checkout_view(request):
	customer = request.user.customer
	if request.method == "POST":
		order = Order(
			owner=customer,
			delivery_is_on=request.data['delivery']
		)
		order.save()
		order.items.add(customer.orders.all())
		order.save()
		return Response(data=OrderSerializer(order).data)

	cart_items = customer.cart.all()
	total = (
			calc_subtotal(cart_items) +
			calc_deivery_fee(cart_items) +
			calc_vat(cart_items) + 
			calc_processing_fee(cart_items)
		)
	data = {
		'subtotal': str(round(calc_subtotal(cart_items), 2)),
		'fees': [
			{
				'type': 'Delivery fee',
				'amount': str(round(calc_deivery_fee(cart_items), 2))
			},
			{
				'type': 'Service fee',
				'amount': str(round(calc_processing_fee(cart_items), 2))
			},
			{
				'type': 'VAT',
				'amount': str(round(calc_vat(cart_items), 2))
			},
		],
		'items': OrderItemSerializer(cart_items.order_by('-id'), many=True).data,
		'total': str(round(total, 2))
	}
	return Response(data=data)


@api_view(["GET", "POST"])
def leave_a_review(request):
	if request.method == "POST":
		review = Review(
			by=request.user,
			rating=request.data['stars'],
			food=FoodItem.objects.get(id=request.data['item']),
			comment=request.data['comment']
		)
		review.save()
		return Response(data={'error': None, 'response_text': 'Successfully reviewed item'})

	# GET : check if a user has reviewed this item
	try:
		review = Review.objects.get(
			by= request.user,
			food=FoodItem.objects.get(id=request.GET.get('item', None)),
			)
		res = {
			'error': None,
			'user_has_review' : True,
			'reviews': ReviewSerializer(
				Review.objects.filter(
					food=FoodItem.objects.get(
						id = request.GET.get('item', None)
					)),
				many=True).data
		}
	except Review.DoesNotExist:
		res = {
			'error': None,
			'user_has_review' : False,
			'reviews': ReviewSerializer(
				Review.objects.filter(
					food=FoodItem.objects.get(
						id = request.GET.get('item', None)
					)),
				many=True).data

		}
	return Response(status=200, data=res)



@api_view(["GET"])
def notifications_view(request):
	try:
		nots = Notification.objects.filter(to=request.user.customer)
		_list = NotificationSerializer(nots, many=True).data
		return Response({'error': None, 'notifications': _list})
	except Exception as e:
		return Response({'error': True, 'error_text': str(e)})
