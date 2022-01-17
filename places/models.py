from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .utils.helpers import generate_staff_id, generate_invoice_id
from rest_framework.authtoken.models import Token



class UserManager(BaseUserManager):
	def create_user(self, first_name, last_name, email, password):
		user = self.model(
			first_name=first_name,
			last_name=last_name,
			email=email,
			password=password
		)
		user.save()
		user.set_password(password)
		user.save()


	def create_superuser(self, first_name, last_name, email, password):
		user = self.model(
			first_name=first_name,
			last_name=last_name,
			email=email,
			password=password,
			is_superuser=True,
			is_staff=True
		)
		user.save()
		user.set_password(password)
		user.save()


class User(AbstractBaseUser):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.CharField(max_length=100, unique=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	date_joined = models.DateField(auto_now=True)
	last_login = models.DateTimeField(blank=True, null=True)
	is_active = True
	objects = UserManager()

	REQUIRED_FIELDS = ['first_name', 'last_name']
	USERNAME_FIELD = 'email'

	def fullname(self):
		return self.first_name + ' ' + self.last_name

	def has_perm(self, perm, obj=None):
		if self.is_superuser:
			return True
		return False

	def has_perms(self, perms):
		if self.is_superuser:
			return True
		return False

	def has_module_perms(self, perms):
		if self.is_superuser:
			return True
		return False

	def token(self):
		key = Token.objects.get_or_create(user=self)[0].key
		return key



class StaffPermission(models.Model):
	code_name = models.CharField(max_length=150)
	verbose_name = models.CharField(max_length=150)

	def __str__(self):
		return self.verbose_name



class Staff(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	staff_id = models.CharField(default=generate_staff_id, max_length=20)
	permissions = models.ManyToManyField(StaffPermission, blank=True)

	def has_perm(self, perm):
		try:
			perm = StaffPermissions.objects.get(code_name=perm)
		except StaffPermissions.DoesNotExist:
			return False
		else:
			if perm in self.permissions.all():
				return True



class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	verified_email = models.BooleanField(default=False)
	phone = models.CharField(max_length=20, blank=True, null=True)
	photo = models.ImageField(upload_to="people/", blank=True, null=True)
	cart = models.ManyToManyField("OrderItem", blank=True)
	orders = models.ManyToManyField("Order", blank=True)

	def __str__(self):
		return self.user.first_name

	def __repr__(self):
		return '<Customer {user}>'.format(user=self.user.first_name)


class Notification(models.Model):
	icon = models.CharField(max_length=20)
	message = models.TextField()


class OrderItem(models.Model):
	item = models.ForeignKey("FoodItem", on_delete=models.CASCADE)
	customizations = models.ManyToManyField("OrderCustomization", blank=True)



class OrderCustomization(models.Model):
	customization = models.ForeignKey("Customization", on_delete=models.CASCADE)
	option = models.ForeignKey("CustomizationOption", on_delete=models.CASCADE)


class Order(models.Model): 
	ORDER_STATUS = (
		('pending', 'Pending'),
		('on-route', 'On Route'),
		('delivered', 'Delivered'),
	)
	owner = models.ForeignKey("Customer", on_delete=models.CASCADE)
	items = models.ManyToManyField(OrderItem, blank=True)
	cleared = models.BooleanField(default=False) # delivery_status
	status = models.CharField(choices=ORDER_STATUS, max_length=20, blank=True, null=True)
	delivery = models.BooleanField(default=False)
	invoice_id = models.CharField(max_length=12, default=generate_invoice_id)
	paid = models.BooleanField(default=False)


def parse_image_url(image):
	return 'http://localhost:8000' + image.image.url


class FoodItem(models.Model):
	title = models.CharField(max_length=150)
	subtitle = models.CharField(max_length=150, blank=True, null=True)
	customizations = models.ManyToManyField("Customization", blank=True)
	about = models.TextField(blank=True, null=True)
	images = models.ManyToManyField("FoodImage", blank=True)
	price = models.DecimalField(decimal_places=2, max_digits=1000)
	packed_with = models.ManyToManyField("Associated", blank=True)
	category = models.CharField(max_length=20, blank=True, null=True)
	tags = models.CharField(max_length=200, blank=True, null=True)

	def get_reviews(self):
		pass

	def average_rating(self):
		stars = []
		for review in self.get_reviews():
			stars.append(review.rating)
		return

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
	image = models.ImageField(upload_to='food/')

	def delete(self):
		os.remove(os.path.abspath(image.path))
		super().delete()


class Customization(models.Model):
	title = models.CharField(max_length=150)
	options = models.ManyToManyField("CustomizationOption", blank=True)

	def __str__(self):
		try:
			return self.food_item.name + ' - ' + self.title
		except:
			return self.title


class CustomizationOption(models.Model):
	option = models.CharField(max_length=100)
	price = models.DecimalField(decimal_places=2, max_digits=1000, blank=True)

	def __str__(self):
		return self.option


class Associated(models.Model):
	name = models.CharField(max_length=150, blank=True, null=True)


class Review(models.Model):
	by = models.ForeignKey(User, on_delete=models.CASCADE)
	food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
	rating = models.IntegerField()
	comment = models.CharField(max_length=500, blank=True, null=True)

	def __str__(self):
		return self.by.first_name + ' review on : ' + self.food.title

