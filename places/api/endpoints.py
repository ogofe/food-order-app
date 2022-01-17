from django.urls import path
from .handlers import (
	IndexView,
	CreateFoodItemView,
	EditFoodItemView,
	ListFoodItemView,
	SignupView,
	LoginView,
	FoodListView,
	list_all_food,
	item_detail_view,
	cart_view
)

app_name = 'api'

urlpatterns = [
	# authentication
	path('signup/', SignupView.as_view()),
	path('login/', LoginView.as_view()),

	# customer
	path('menu/', list_all_food),
	path('menu/<pk>/', item_detail_view),
	path('cart/', cart_view),
	path('checkout/', EditFoodItemView.as_view()),
	path('pay/', EditFoodItemView.as_view()),
]