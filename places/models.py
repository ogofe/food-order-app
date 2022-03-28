from django.db import models
from django.contrib.auth.models import User, Permission
from .utils.helpers import (
	generate_staff_id,
	generate_invoice_id,
	get_average_rating,
	parse_image_url,
)
from rest_framework.authtoken.models import Token
from decimal import Decimal


class Staff(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	staff_id = models.CharField(default=generate_staff_id, max_length=20)

	@property
	def permissions(self):
		return self.user.permissions.all()

	def grant_permission(self, perm):
		return

	def revoke_permission(self, perm):
		return


class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	verified_email = models.BooleanField(default=False)
	phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
	photo = models.ImageField(upload_to="people/", blank=True, null=True)
	cart = models.ManyToManyField("OrderItem", blank=True)
	orders = models.ManyToManyField("Order", blank=True)
	is_app_user = models.BooleanField(default=True)

	def joined(self):
		return self.user.date_joined

	def __str__(self):
		return self.user.username

	def __repr__(self):
		return '<Customer {user}>'.format(user=self.user.first_name)



class Notification(models.Model):
	to = models.ForeignKey(Customer, on_delete=models.CASCADE)
	msg_type = models.CharField(max_length=20)
	message = models.TextField()



class OrderItem(models.Model):
	item = models.ForeignKey("FoodItem", on_delete=models.CASCADE)
	qty = models.IntegerField(default=1)
	customizations = models.ManyToManyField("OrderCustomization", blank=True)

	def __str__(self):
		return self.item.title

	@property
	def total(self):
		num = (self.item.price * self.qty)
		for custom in self.customizations.all():
			num += custom.option.price
		return Decimal(num)


class OrderCustomization(models.Model):
	customization = models.ForeignKey("Customization", on_delete=models.CASCADE)
	option = models.ForeignKey("CustomizationOption", on_delete=models.CASCADE)

	def __str__(self):
		return self.customization.title



class Order(models.Model): 
	ORDER_STATUS = (
		('pending', 'Pending'),
		('on-route', 'On Route'),
		('delivered', 'Delivered'),
	)
	owner = models.ForeignKey("Customer", on_delete=models.CASCADE)
	created_on = models.DateTimeField(auto_now=True)
	items = models.ManyToManyField(OrderItem, blank=True)
	delivered = models.BooleanField(default=False) # delivery_status
	status = models.CharField(choices=ORDER_STATUS, max_length=20, default='pending')
	delivery_is_on = models.BooleanField(default=False)
	invoice = models.CharField(max_length=12, blank=True, null=True, default=generate_invoice_id, unique=True)
	paid = models.BooleanField(default=False)

	def __str__(self):
		return self.invoice_id

	def subtotal(self):
		num = 0
		for item in items.all():
			num += item.total
		return Decimal(num)



class Tag(models.Model):
	tag = models.CharField(max_length=50, unique=True)

	def __str__(self):
		return self.tag



class Category(models.Model):
	name = models.CharField(max_length=50, unique=True)

	def __str__(self):
		return self.name


class FoodItem(models.Model):
	title = models.CharField(max_length=150, unique=True)
	subtitle = models.CharField(max_length=150, blank=True, null=True)
	customizations = models.ManyToManyField("Customization", blank=True, related_name="customizations")
	about = models.TextField(blank=True, null=True)
	images = models.ManyToManyField("FoodImage", blank=True, related_name="images")
	price = models.DecimalField(decimal_places=2, max_digits=1000)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
	tags = models.ManyToManyField(Tag, blank=True)
	reviews = models.ManyToManyField("Review", blank=True, related_name="reviews")
	featured = models.BooleanField(default=False)

	def rating(self):
		from .models import Review
		reviews = Review.objects.filter(food=self)
		rate = get_average_rating(reviews)
		return rate

	def __str__(self):
		return self.title

	def image(self):
		imgs = list(self.images.all())
		if len(imgs) > 0:
			return parse_image_url(imgs[0])
		return None

	def get_absolute_url(self, *args, **kwargs):
		from django.urls import reverse
		return reverse('admin:detail', {'pk': self.pk})



class FoodImage(models.Model):
	item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='food/')

	def delete(self):
		os.remove(os.path.abspath(image.path))
		super().delete()

	@property
	def image_url(self):
		if not '.herokuapp.com' in self.image.url:
			print("setting up media url")
			return 'https://jtogofe-hotspot.herokuapp.com' + self.image.url
		return self.image.url
	


class Customization(models.Model):
	food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
	title = models.CharField(max_length=150, unique=True)
	options = models.ManyToManyField("CustomizationOption", blank=True, related_name="choices")
	required = models.BooleanField(default=False)
	default_option = models.ForeignKey("CustomizationOption", blank=True, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		try:
			return self.food_item.name + ' - ' + self.title
		except:
			return self.title


class CustomizationOption(models.Model):
	to = models.ForeignKey(Customization, on_delete=models.CASCADE)
	option = models.CharField(max_length=100, unique=True)
	price = models.DecimalField(decimal_places=2, max_digits=1000, blank=True)

	def __str__(self):
		return self.option


class Review(models.Model):
	by = models.ForeignKey(User, on_delete=models.CASCADE)
	food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
	rating = models.IntegerField()
	comment = models.CharField(max_length=500, blank=True, null=True)

	def reviewer(self):
		return self.by.get_full_name()

	def __str__(self):
		return self.by.first_name + ' review on : ' + self.food.title

