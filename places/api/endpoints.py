from django.urls import path
from .handlers import (
	SignupView,
	login_view,
	menu_view,
	item_detail_view,
	cart_view,
	search_view,
	checkout_view,
	notifications_view,
	leave_a_review,
)

app_name = 'api'

urlpatterns = [
	# authentication
	path('signup/', SignupView.as_view()),
	path('login/', login_view),

	# customer
	path('me/', menu_view),
	path('notifications/', notifications_view),
	path('menu/', menu_view),
	path('find/', search_view),
	path('menu/<pk>/', item_detail_view),
	path('cart/', cart_view),
	path('checkout/', checkout_view),
	path('rate/', leave_a_review),
]