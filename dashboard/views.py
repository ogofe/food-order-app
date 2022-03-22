import os, json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import (
	CreateAPIView,
	ListAPIView,
	RetrieveUpdateDestroyAPIView,
	DestroyAPIView,
)
from django.db.models import Q
from rest_framework.response import Response
from places.api.serializers import (
	FoodSerializer,
	CustomerSerializer,
	CategorySerializer,
	TagSerializer,
	OrderSerializer,
	OrderItemSerializer,
	ReviewSerializer,
	UserSerializer,
	PermissionSerializer,
	StaffSerializer,
)
from django.contrib.auth import authenticate
from places.models import *
from rest_framework.decorators import api_view



@api_view(["POST"])
def login_view(request):
	try:
		user = authenticate(username=request.data['username'], password=request.data['password'])
		if user:
			data = {
				'user': UserSerializer(user).data,
				'token': Token.objects.get_or_create(user=user)[0].key,
			}
			return Response({'error': None, 'user_profile': data})
		return Response({'error': None, 'error_text': "User not found"}, status=404)
	except Exception as e:
		return Response({'error': None, 'error_text': "User not found"}, status=404)


class DashboardView(APIView):
	def get(self, request):
		data = {
			'help': None,
		}
		return Response(data=data)


class CreateFoodItemView(CreateAPIView):
	serializer_class = FoodSerializer

	def get(self, request):
		data = {
			'error': None,
			'tags': TagSerializer(Tag.objects.all(), many=True).data,
			'categories': CategorySerializer(Category.objects.all(), many=True).data,
		}
		return Response(data)

	def post(self, request, **kwargs):
		print(request.data)
		try:
			food_item = FoodItem(
					title=request.data['title'],
					subtitle=request.data['subtitle'],
					price=request.data['price'],
					category=Category.objects.get(name=request.data['category']),
					about=request.data['about']
				)
			food_item.save()

			for customization in request.data.getlist('customization', []):
				customization = json.loads(customization)
				change = Customization(
					food=food_item,
					title=customization['title'],
					required=True if customization['required'] == "on" else False,
					)
				change.save()

				for option in customization['options']:
					choice = CustomizationOption(
						to=change,
						option=option['name'],
						price=option['price']
					)
					choice.save()
					if customization.get('default_option', None) == choice.option:
						change.default_option = choice
					change.options.add(choice)
				change.save()
				food_item.customizations.add(change)

			for _tag in request.data.getlist('tags', None):
				tag = Tag.objects.get(tag=_tag)
				food_item.tags.add(tag)

			for image in request.FILES.getlist('image'):
				food_image = FoodImage(item=food_item, image=image)
				food_image.save()
				food_item.images.add(food_image)
			food_item.save()
			return Response({'error': None, 'item': self.serializer_class(food_item).data})
		except Exception as e:
			# raise e
			return Response({'error': True, 'error_text': str(e)}, status=500)



class EditFoodItemView(RetrieveUpdateDestroyAPIView):
	queryset = FoodItem.objects.all()
	serializer_class = FoodSerializer
	lookup_field = 'pk'

	def post(self, request, **kwargs):
		food_item = FoodItem.objects.get(id=kwargs['pk'])
		action = request.data.get('action', None)

		if action and action == "remove-choice":
			pass # del the customization
		elif action and action == "remove-option":
			pass # del a customization optio
		elif action and action == "remove-image":
			pass # del a customization option
		else: # saving the product changes
			pass
		return Response({'error': None})




class ListFoodItemView(ListAPIView):
	model = FoodItem
	serializer_class = FoodSerializer

	def get(self, request):
		queryset = self.model.objects.all()
		if request.GET.get('find', None):
			queryset = queryset.filter()
		data = {
			'error': None,
			'results': FoodSerializer(queryset, many=True).data,
		}
		return Response(data)

	def post(self, request):
		return Response()

	def delete(self, request):
		for item in request.data.get('items', None):
			food = FoodItem.objects.get(id=item)
			food.delete()
		return Response({'error': None, 'response_text': 'Successfully deleted products'})


class ManagerView(APIView):

	def get(self, request):
		resource = request.GET.get('res', None)
		if not resource:
			return Response({'error': True, 'error_text': 'specify resource param with ?res=<resource>'}, status=500)
		elif resource == "categories":
			data = CategorySerializer(Category.objects.all(), many=True).data
		elif resource == "tags":
			data = TagSerializer(Tag.objects.all(), many=True).data
		return Response({'error': None, 'data': data})

	def post(self, request):
		res = request.GET.get('res', None)
		action = request.data.get('action', None)
		if not res:
			return Response({'error': True, 'error_text': 'specify resource param with ?res=<resource>'}, status=500)
		if not action:
			return Response({'error': True, 'error_text': 'specify action in your request'}, status=500)
		if res == "categories":
			if action == 'delete':
				category = Category.objects.get(name=request.data['name'])
				category.delete()
				return Response({'error': None, 'response_text': 'Tag deleted'})
			elif action == 'add':
				category = Category.objects.create(name=request.data['name'])
			elif action == 'edit':
				category = Category.objects.get(tag=request.data['name'])
				category.name = request.data['name']
				category.save()
			return Response({'error': None, 'tag': CategorySerializer(category).data})
		elif res == "tags":
			if action == 'delete':
				tag = Tag.objects.get(tag=request.data['name'])
				tag.delete()
				return Response({'error': None, 'response_text': 'Tag deleted'})
			elif action == 'add':
				tag = Tag.objects.create(tag=request.data['name'])
			elif action == 'edit':
				tag = Tag.objects.get(tag=request.data['name'])
				tag.tag = request.data['name']
				tag.save()
			return Response({'error': None, 'tag': TagSerializer(tag).data})
		return Response(status=500)



class CreateOrderView(CreateAPIView):

	def get(self, request):
		data = {
			'error': None,
			'products': FoodSerializer(FoodItem.objects.all(), many=True).data,
			'customers': CustomerSerializer(Customer.objects.all(), many=True).data,
		}
		return Response(data, status=200)


	def post(self, request, **kwargs):
		try:
			data = request.data
			print(request.data)
			customer = Customer.objects.get(phone=data['customer'])
			order = Order(
					owner = customer,
					delivery_is_on=True if data['delivery'] == 'delivery' else False,
				)
			order.save()

			for item in data['items']:
				order_item = OrderItem(
					item = FoodItem.objects.get(title=item['product']),
					qty = item['qty'],
				)
				order_item.save()

				for customization in item.get('customizations', None):
					print("Customization:", customization)
					custom = Customization.objects.get(title=customization['customize'], food=order_item.item)
					option = CustomizationOption.objects.get(to=custom, option=customization['choice'])
					customize = OrderCustomization(
						customization = custom,
						option = option
					)
					customize.save()
					order_item.customizations.add(customize)
					order_item.save()
				order.items.add(order_item)
			order.save()
			customer.orders.add(order)
			customer.save()
			return Response({'error': None, 'order': OrderSerializer(order).data})
		except Exception as e:
			return Response({'error': True, 'error_text': str(e)})


class OrderDetailView(APIView):
	def get(self, request, invoice):
		try:
			order = Order.objects.get(invoice=invoice)
			data = {
				'error': None,
				'order': OrderSerializer(order).data
			}
			return Response(data)
		except Exception as e:
			data = {'error': True, 'error_text': str(e)}
			return Response(data)


class EditOrderView(RetrieveUpdateDestroyAPIView):
	queryset = FoodItem.objects.all()
	serializer_class = FoodSerializer
	lookup_field = 'pk'

	def post(self, request, **kwargs):
		return Response()



class ListOrdersView(ListAPIView):

	def delete(self, request):
		for item in request.data['items']:
			order = Order.objects.get(id=item)
			order.delete()
		return Response({'error': None, 'response_text': "Successfully deleted order"})

	def get(self, request):
		orders = OrderSerializer(Order.objects.all(), many=True).data
		data = {
			'error': None,
			'results': orders
		}
		return Response(data)


class ListCustomersView(ListAPIView):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer

	def get(self, request):
		customers = CustomerSerializer(Customer.objects.all(), many=True).data
		data = {
			'error': None,
			'results': customers
		}
		return Response(data)


class CreateCustomerView(CreateAPIView):
	def post(self, request):
		try:
			user = User(
				first_name=request.data['first_name'],
				last_name=request.data['last_name'],
				username=str(os.urandom(6).hex()),
				email=request.data['email'],
			)
			user.save()
			user.set_unusable_password()
			customer = Customer(
				user=user,
				phone=request.data['phone'],
			)
			customer.save()
			return Response({'error': None, 'customer' : CustomerSerializer(customer).data})
		except Exception as e:
			return Response({'error': True, 'error_text': str(e)}, status=500)



class ListStaffView(ListAPIView):
	def get(self, request):
		staff = StaffSerializer(Staff.objects.all(), many=True).data
		data = {
			'error': None,
			'staff': staff
		}
		return Response(data)


class CreateStaffView(APIView):

	def get(self, request):
		perms = Permission.objects.all().filter(
			content_type__model__in=[
			'fooditem', 'customer',
			'staff', 'order',
			])
		data = {
			'error': None, 
			'permissions': PermissionSerializer(perms, many=True).data
		}
		return Response(data)

	def post(self, request):
		try:
			staff_id = generate_staff_id()
			user = User(
					email=request.data['email'],
					username=staff_id,
					first_name=request.data['first_name'],
					last_name=request.data['last_name'],
				)
			user.save()
			user.set_unusable_password()
			staff = Staff(
					user = user,
					staff_id=staff_id
				)
			staff.save()
			return Response({'error': None, 'staff': StaffSerializer(staff).data})
		except Exception as e:
			return Response({'error': None, 'error_text': str(e)})




class ListNotificationsView(ListAPIView):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer

	def get(self, request):
		customers = CustomerSerializer(Customer.objects.all(), many=True).data
		data = {
			'error': None,
			'results': customers
		}
		return Response(data)
