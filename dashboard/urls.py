from django.urls import path
from .views import (
	DashboardView,
	CreateFoodItemView,
	ListFoodItemView,
	EditFoodItemView,
	ListCustomersView,
	CreateCustomerView,
	ListOrdersView,
	OrderDetailView,
	CreateOrderView,
	CreateStaffView,
	ListStaffView,
	ManagerView,
	login_view,
)

app_name = 'dashboard'

urlpatterns = [
	path('login/', login_view),
	path('dashboard/', DashboardView.as_view()),
	path('manage/', ManagerView.as_view()),
	path('products/', ListFoodItemView.as_view()),
	path('products/add/', CreateFoodItemView.as_view()),
	path('products/<pk>/change/', EditFoodItemView.as_view()),
	path('customers/', ListCustomersView.as_view()),
	path('customers/add/', CreateCustomerView.as_view()),
	path('orders/', ListOrdersView.as_view()),
	path('orders/<invoice>/', OrderDetailView.as_view()),
	path('orders/add/', CreateOrderView.as_view()),
	path('staff/', ListStaffView.as_view()),
	path('staff/add/', CreateStaffView.as_view()),

]